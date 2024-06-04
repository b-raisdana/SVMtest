import datetime

import numpy as np
import pandas as pd

from generating_random_data import config
from generating_random_data.distribution import gaussian
from generating_random_data.logins import logins, more_login_to_self_workstations

daily_timesheet = pd.read_csv("shift_employees.csv", parse_dates=['Day'])


# def choose_normal_starters(_daily_timesheet):
#     list_of_users = _daily_timesheet['UserID'].unique().tolist()
#     # choose 'normal_starters'. they are always the same.
#     number_of_normal_starters = round(config.normal_starters * len(list_of_users))
#     _normal_starters = np.random.choice(list_of_users, number_of_normal_starters, replace=False)
#     return _normal_starters


# normal_starters = choose_normal_starters(daily_timesheet)


# def first_login_to_self_workstation(_daily_timesheet, _normal_starters):
#     # choose 'normal_starters_start_at_shift_start' days.
#
#     number_of_normal_starters_at_shift_start = round(
#         config.normal_starters_start_at_shift_start * len(_normal_starters))
#     normal_starters_at_shift_start = np.random.choice(_normal_starters, number_of_normal_starters_at_shift_start,
#                                                       replace=False)
#     normal_starters_at_shift_start_mask = _daily_timesheet['UserID'].isin(normal_starters_at_shift_start)
#     scheduled_starts = _daily_timesheet.loc[normal_starters_at_shift_start_mask, 'Shift Start']
#     tolerance_start_mins = gaussian(start=config.normal_early_start_mins, end=config.normal_late_start_mins,
#                                     size=number_of_normal_starters_at_shift_start, skew=10)
#     actual_starts = scheduled_starts + tolerance_start_mins * datetime.timedelta(minutes=1)
#     _daily_timesheet.loc[normal_starters_at_shift_start_mask, 'Actual Start'] = actual_starts
#     return _daily_timesheet
#
#
# actual_start(daily_timesheet, daily_timesheet['UserID'].unique())


# '''
# choose start time of 'normal_starters_start_at_shift_start' days according to 'role_shift_varieties'.
# add the tolerance of 'normal_starters_start_at_shift_start_late_start_tolerance_mins'
# '''
#
# '''
# choose start time of other days of 'normal_starters' according to 'role_shift_varieties'.
# add the tolerance of 'normal_early_start_mins' and 'normal_late_start_mins'
# '''
#
# '''
# choose start time of other days of other employees according to 'role_shift_varieties' by skewed, kurtosis distribution.
# '''
def drop_absents(_daily_timesheet: pd.DataFrame):
    # remove absents according to 'absence_rate' weighted distributed between roles and shifts.
    role_absent_counts = dict(zip(
        config.roles.keys(),
        np.random.multinomial(round(config.absence_rate * config.total_employees),
                              [config.role_distribution[role] for role in config.roles])))
    for day in _daily_timesheet['Day'].unique():
        d_work_group_mask = _daily_timesheet['Day'] == day
        for role in config.roles:
            day_roles_mask = d_work_group_mask & (_daily_timesheet['Role'] == role)
            day_roles_idxs = _daily_timesheet.loc[day_roles_mask].index
            role_absents = np.random.choice(day_roles_idxs, role_absent_counts[role])
            _daily_timesheet.drop(role_absents, axis='index')


drop_absents(daily_timesheet)



