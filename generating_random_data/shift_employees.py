import datetime
from random import randint

import numpy as np
import pandas as pd

import config
from work_groups import work_group_df


def generate_daily_timesheet(_work_group_df):
    '''
    assign per-day shifts and roles to employees according to 'role_shift_varieties'.
    first assume roles and shifts does not change.
    '''
    _daily_timesheet = (
        _work_group_df.merge(
            pd.DataFrame(
                {'Day': pd.date_range(config.start_day, datetime.timedelta(days=config.duration_days), freq='1d')}),
            how='cross'))
    return _daily_timesheet


daily_timesheet = generate_daily_timesheet(work_group_df)


def role_change(_daily_timesheet):
    '''
    candidate users to change their role according to 'employee_role_change' and 'employee_role_change_min_duration_days'. 
    '''
    role_change_candidates = (
        np.random.choice(len(work_group_df),
                         config.employee_weekly_role_change_rate * (config.duration_days / 7) * len(work_group_df),
                         replace=False))
    role_change_date_offsets = np.random.choice(config.duration_days, len(role_change_candidates), replace=True)
    role_change_dates = [config.start_day + datetime.timedelta(days=day_offset) for day_offset in
                         role_change_date_offsets]
    for i, user_index in enumerate(role_change_candidates):
        user_id = work_group_df.iloc[user_index]['UserID']
        user_role = work_group_df.iloc[user_index]['Role']
        _daily_timesheet[
            (_daily_timesheet['UserID'] == user_id) &
            (_daily_timesheet['Day'] > role_change_dates[i])
            ] = config.roles.remove(user_role)[randint(len(config.roles) - 1)]


role_change(daily_timesheet)


def daily_role_shifts(_daily_timesheet):
    '''
    distribute role shifts according to daily employee's roles.
    '''
    for day in _daily_timesheet['Day'].unique():
        all_shifts_of_the_day_index = _daily_timesheet[
            (_daily_timesheet['Day'] == day) &
            (_daily_timesheet['Rol'].isin(['Support Shift', 'Regular Shift']))
            ].index
        _daily_timesheet.loc[all_shifts_of_the_day_index, 'Shift'] = \
            np.random.choice(['morning', 'afternoon', 'night'], len(all_shifts_of_the_day_index), replace=True)


daily_role_shifts(daily_timesheet)


def shift_change(_daily_timesheet):
    '''
    candidate users to change their shift according to 'employee_shift_change', 'employee_shift_change_min_duration_days', 
    and 'employee_shift_change_min_duration_days'. 
    '''
    # duration_days = - daily_timesheet['Day'].min()
    days_of_shift_change = np.random.choice(
        pd.date_range(_daily_timesheet['Day'].min(), _daily_timesheet['Day'].max()),
        size=randint(3, config.duration_days), replace=True)
    shift_changes_per_days = np.random.multinomial(
        config.employee_shift_change_rate * config.duration_days * config.total_employees,
        [1 / len(days_of_shift_change)] * len(days_of_shift_change))
    number_of_shifts_to_change = (
        np.random.randint(-2, 2, config.employee_shift_change_rate * config.duration_days * config.total_employees))
    for i, day_offset in enumerate(days_of_shift_change):
        shift_change_idxs = _daily_timesheet[
            (_daily_timesheet['Day'] == config.start_day + datetime.timedelta(days=day_offset)) &
            (_daily_timesheet['Rol'].isin(['Support Shift', 'Regular Shift']))
            ].index
        consumed_shift_changes = sum(shift_changes_per_days[:i])
        t_number_of_shifts_to_change = \
            number_of_shifts_to_change[consumed_shift_changes: consumed_shift_changes + shift_changes_per_days]
        _daily_timesheet.iloc[shift_change_idxs]['Shift'] = \
            (_daily_timesheet.iloc[shift_change_idxs]['Shift'] + t_number_of_shifts_to_change % 3)


shift_change(daily_timesheet)
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
