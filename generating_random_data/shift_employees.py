import datetime
from random import randint

import numpy as np
import pandas as pd

import config
from work_groups import work_group_df, is_sized_work_group


def diff(df1, df2):
    return (df1 != df2)[(df1 != df2).any(axis=1)]


def generate_daily_timesheet(_work_group_df):
    '''
    assign per-day shifts and roles to employees according to 'role_shift_varieties'.
    first assume roles and shifts does not change.
    '''
    _daily_timesheet = (
        _work_group_df.merge(
            pd.DataFrame(
                {'Day': pd.date_range(config.start_day,
                                      config.start_day + datetime.timedelta(days=config.duration_days),
                                      freq='1d')}),
            how='cross'))
    return _daily_timesheet


daily_timesheet = generate_daily_timesheet(work_group_df)


def verify_daily_timesheet(d_t):
    assert all(
        [is_sized_work_group(
            d_t[d_t['Day'] == day].groupby(['Role']).size().reset_index().rename(columns={0: 'Population'}))
            for day in d_t['Day'].unique()])


verify_daily_timesheet(daily_timesheet)


def role_change(_daily_timesheet, _work_group):
    '''
    candidate users to change their role according to 'employee_role_change' and 'employee_role_change_min_duration_days'. 
    '''
    _daily_timesheet_back = _daily_timesheet.copy()
    role_change_candidates = (
        np.random.choice(work_group_df['UserID'],
                         int(config.employee_weekly_role_change_rate * (config.duration_days / 7) * len(work_group_df)),
                         replace=False))
    role_change_dates = np.random.choice(_daily_timesheet['Day'].unique(), len(role_change_candidates), replace=True)
    for i, user_id in enumerate(role_change_candidates):
        user_role = _work_group.loc[_work_group['UserID'] == user_id, 'Role'].values[0]
        _daily_timesheet.loc[
            (_daily_timesheet['UserID'] == user_id) &
            (_daily_timesheet['Day'] > role_change_dates[i])
            , 'Role'
        ] = config.roles[(config.roles.index(user_role) + 1) % len(config.roles)]
    changes = diff(_daily_timesheet_back, _daily_timesheet)
    nop = 1


daily_timesheet_back = daily_timesheet.copy()
role_change(daily_timesheet, work_group_df)
changes = diff(daily_timesheet_back, daily_timesheet)
verify_daily_timesheet(daily_timesheet)


# def daily_role_shifts_of_support_and_regular(_daily_timesheet):
#     '''
#     distribute role shifts according to daily employee's roles.
#     '''
#     for day in _daily_timesheet['Day'].unique():
#         all_shifts_of_the_day_index = _daily_timesheet[
#             (_daily_timesheet['Day'] == day) &
#             (_daily_timesheet['Role'].isin(['Support Shift', 'Regular Shift']))
#             ].index
#         _daily_timesheet.loc[all_shifts_of_the_day_index, 'ShiftID'] = \
#             np.random.randint(0, len(config.all_shifts), len(all_shifts_of_the_day_index)).tolist()
#         # _daily_timesheet.loc[all_shifts_of_the_day_index].groupby('Shift').size()
#     return _daily_timesheet
#
#
# daily_timesheet = daily_role_shifts_of_support_and_regular(daily_timesheet)
# assert not daily_timesheet[daily_timesheet['Role'].isin(['Support Shift', 'Regular Shift'])]['ShiftID'].isna().any()
# verify_daily_timesheet(daily_timesheet)

# remained_shift_roles = daily_timesheet[daily_timesheet['ShiftID'].isna()]['Role'].unique()  # ['Admin' 'Support Day' 'Regular Day']


def daily_role_shifts(_daily_timesheet: pd.DataFrame):
    if 'ShiftID' in daily_timesheet.columns:
        roles_to_assign_shifts = _daily_timesheet[daily_timesheet['ShiftID'].isna()]['Role'].unique()
    else:
        roles_to_assign_shifts = config.roles
    for role in roles_to_assign_shifts:
        role_timesheet_mask = _daily_timesheet['Role'] == role
        # role_timesheet_idx = _daily_timesheet[_daily_timesheet['Role'] == role].index
        role_shift_varieties = config.role_shift_varieties[role]
        role_shift_variety_names = role_shift_varieties.keys()
        role_shift_variety_proportion = [proportion for shift_time_dict, proportion in role_shift_varieties.values()]
        for day in _daily_timesheet['Day'].unique():
            all_shifts_of_the_day_index = _daily_timesheet[role_timesheet_mask & (_daily_timesheet['Day'] == day)].index
            if len(role_shift_variety_names) > 1:
                _daily_timesheet.loc[all_shifts_of_the_day_index, 'ShiftID'] = \
                    np.random.choise(range(len(role_shift_variety_names)), len(all_shifts_of_the_day_index),
                                     p=role_shift_variety_proportion).tolist()
            else:
                _daily_timesheet.loc[all_shifts_of_the_day_index, 'ShiftID'] = 0


daily_timesheet = daily_role_shifts(daily_timesheet)
assert not daily_timesheet[daily_timesheet['Role'].isin(['Support Shift', 'Regular Shift'])]['ShiftID'].isna().any()
assert not daily_timesheet[daily_timesheet['Role'].isin(['Support Shift', 'Regular Shift'])]['ShiftID'].isna().any()
verify_daily_timesheet(daily_timesheet)


def shift_change(_daily_timesheet):
    '''
    candidate users to change their shift according to 'employee_shift_change', 'employee_shift_change_min_duration_days', 
    and 'employee_shift_change_min_duration_days'. 
    '''
    # _daily_timesheet_back = _daily_timesheet.copy()
    days_of_shift_change = np.random.choice(
        pd.date_range(_daily_timesheet['Day'].min(), _daily_timesheet['Day'].max()),
        size=randint(int(len(_daily_timesheet['Day'].unique()) * (3 / 4)), len(_daily_timesheet['Day'].unique())),
        replace=True)
    shift_changes_per_days = np.random.multinomial(
        config.employee_shift_change_rate * config.duration_days * config.total_employees,
        [1 / len(days_of_shift_change)] * len(days_of_shift_change))
    number_of_shifts_to_change = (
        np.random.choice([-2, -1, 1, 2],
                         int(config.employee_shift_change_rate * config.duration_days * config.total_employees)))
    for i, day in enumerate(days_of_shift_change):
        day_shifts = _daily_timesheet[
            (_daily_timesheet['Day'] == day) &
            (_daily_timesheet['Role'].isin(['Support Shift', 'Regular Shift']))
            ].index
        shift_change_idxs = np.random.choice(day_shifts, shift_changes_per_days[i], replace=False)
        consumed_shift_changes = sum(shift_changes_per_days[:i])
        shifts_of_day_shift_offset = \
            number_of_shifts_to_change[consumed_shift_changes: consumed_shift_changes + shift_changes_per_days[i]]
        # shifts_of_days = _daily_timesheet.iloc[shift_change_idxs]['Shift'].values
        # new_shifts_of_day = [
        #     config.all_shifts[(config.all_shifts.index(shift) + shifter_offset) % len(config.all_shifts)]
        #     for shift, shifter_offset in zip(shifts_of_days, shifts_of_day_shift_offset)]
        _daily_timesheet.iloc[shift_change_idxs]['ShiftID'] = (_daily_timesheet.iloc[shift_change_idxs][
                                                                   'ShiftID'] + shifts_of_day_shift_offset) % 3
    # changes = diff(_daily_timesheet_back,_daily_timesheet)


daily_timesheet_back = daily_timesheet.copy()
shift_change(daily_timesheet)
changes = diff(daily_timesheet_back, daily_timesheet_back)
daily_timesheet_back['Shift'] = daily_timesheet_back['ShiftID'].map(
    {index: value for index, value in enumerate(config.all_shifts)})
# def distribute_role_over_shifts(role, work_group_df):
#     regular_shift_idx = work_group_df[work_group_df['Role'] == role].index.values.tolist()
#     shifts_headcount = np.random.multinomial(
#         range(len(regular_shift_idx)),
#         [(1 / len(config.role_shift_varieties[role]))] * len(config.role_shift_varieties[role]))
#     j = 0
#     for i in range(len(config.role_shift_varieties[role])):
#         work_group_df.iloc[regular_shift_idx[j:shifts_headcount[i]]]['Shift'] = \
#             config.role_shift_varieties[role].keys()[i]
#         j = shifts_headcount[i]
