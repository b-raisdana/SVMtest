import datetime
from typing import Literal

import numpy as np
import pandas as pd

from generating_random_data import config
from generating_random_data.distribution import gaussian

daily_timesheet = pd.read_csv("shift_employees.csv", parse_dates=['Day', 'Shift Start dt', 'Shift End dt'])


def first_login(_daily_timesheet):
    number_of_self_workstation_first_logins = round(
        config.self_workstation_first_login_rate * len(_daily_timesheet))
    self_workstation_first_login_ids = np.random.choice(_daily_timesheet.index, number_of_self_workstation_first_logins,
                                                        replace=False)
    scheduled_start_day = _daily_timesheet.loc[self_workstation_first_login_ids, 'Day']
    # scheduled_start_hours = _daily_timesheet.loc[self_workstation_first_login_ids, 'Shift Start H']
    scheduled_start_hours = pd.to_timedelta(_daily_timesheet.loc[self_workstation_first_login_ids, 'Shift Start H'],
                                            unit='hours')
    tolerance_start_mins = pd.to_timedelta(
        gaussian(start=-config.normal_early_start_mins, end=config.normal_late_start_mins,
                 size=number_of_self_workstation_first_logins, skew=4), unit='minutes')
    login_time = (scheduled_start_day + scheduled_start_hours + tolerance_start_mins)

    _logins = _daily_timesheet.loc[self_workstation_first_login_ids].copy()
    _logins['Target Type'] = 'Self Work Station'
    # fails the test iloc[[0,0]]
    # _logins['Login Target'] = _logins[['UserID', 'GroupID', 'Target Type']].to_records(index=False)
    _logins['Login Time'] = login_time
    return _logins


logins = first_login(daily_timesheet)  # todo: test iloc[[0,0]]


def drop_near_re_logins(_logins: pd.DataFrame):
    _logins.sort_values(by=['UserID', 'Login Time'], ascending=True, inplace=True)
    _logins.reset_index(drop=True, inplace=True)
    # _logins['New Index'] = range(len(_logins))
    # _logins.set_index('New Index', inplace=True)
    _logins['Previous UserID'] = _logins['UserID'].shift(1)
    _logins['Previous Login Time'] = _logins['Login Time'].shift(1)

    near_logins_idxs = _logins.loc[
        (_logins['UserID'] == _logins['Previous UserID']) &
        ((_logins['Login Time'] - _logins['Previous Login Time']) <
         datetime.timedelta(minutes=config.min_inter_login_mins))
        ].index
    _logins.drop(index=near_logins_idxs, axis=0, inplace=True)
    nop = 1


def more_login_to_self_workstations(_daily_timesheet: pd.DataFrame, _logins: pd.DataFrame):
    self_re_login_ilocs = np.random.choice(range(len(_logins)),
                                           round(len(_daily_timesheet) * config.self_workstation_next_login_rate),
                                           replace=True)
    re_logins: pd.DataFrame = _logins.iloc[self_re_login_ilocs].copy()  # todo: test
    re_logins['Login Time'] = generate_login_times(re_logins)
    _logins = pd.concat([_logins, re_logins])
    drop_near_re_logins(_logins)
    return _logins
    # for re_login in re_logins.index:
    #     last_login_of_same_user = _logins.loc[(
    #             (_logins['Day'] == re_logins.loc[re_login, 'Day']) &
    #             (_logins['UserID'] == re_logins.loc[re_login, 'UserID'])
    #     )].sort_by('Login Time').last()
    #     new_login_time = datetime.fromtimestamp(random.randint(
    #         (last_login_of_same_user['Login Time'] + config.min_inter_login_mins).to_datetime().total_seconds(),
    #         last_login_of_same_user['Shift End H'].to_datetime().total_seconds()))
    #     re_logins.loc[re_login, 'Login Time'] = new_login_time
    #     _logins = pd.concat(logins, re_logins.loc[re_login])


def generate_login_times(candidate_shifts: pd.DataFrame):
    seconds_in_shift = (candidate_shifts['Shift End dt'] - candidate_shifts['Shift Start dt']).dt.seconds
    candidate_shifts['Login Seconds Shifter'] = np.random.normal(loc=0, scale=seconds_in_shift / 4, size=len(
        candidate_shifts))  # 95% in shift time with normal distribution
    middle_of_shift = candidate_shifts['Shift Start dt'] + (
            candidate_shifts['Shift End dt'] - candidate_shifts['Shift Start dt']) / 2
    return middle_of_shift + pd.to_timedelta(candidate_shifts['Login Seconds Shifter'], unit='seconds')


logins = more_login_to_self_workstations(daily_timesheet, logins)


def logins_to_other_device(_daily_timesheet: pd.DataFrame, _logins: pd.DataFrame):
    for user_type, user_parameters in config.login_norms.items():  # todo: test
        roles: list = user_parameters['roles']
        rates: dict = user_parameters['rates']

        user_type_timeshift_idx = _daily_timesheet[_daily_timesheet['Role'].isin(roles)].index
        for device_type, device_parameters in rates.items():
            proportion = device_parameters['proportion']
            _max = device_parameters['max']
            chosen_shifts = \
                np.random.choice(user_type_timeshift_idx, round(len(user_type_timeshift_idx) * proportion))
            multiple_login_in_same_shift = np.random.randint(0, _max + 1, len(chosen_shifts))
            # [item for item, count in zip(list1, list2) for _ in range(count)]
            duplicated_shift_ids = \
                [idx for idx, count in zip(chosen_shifts, multiple_login_in_same_shift)
                 for _ in range(count)]
            new_logins = _daily_timesheet.loc[duplicated_shift_ids].copy()
            new_logins['Target Type'] = device_type  # todo: test
            new_logins['Login Time'] = generate_login_times(new_logins)
            _logins = pd.concat([_logins, new_logins])

    drop_near_re_logins(_logins)
    return _logins


logins = logins_to_other_device(daily_timesheet, logins)  # todo: test

devices = pd.read_csv('devices.csv')


def general_role(role):
    for g_role, parameters in config.login_norms.items():
        specific_roles = parameters['roles']
        if role in specific_roles:
            return g_role
    raise ValueError(role)


def self_workstation(sub_logins: pd.DataFrame, _devices):
    # target is UserID.GroupID
    merged = sub_logins.merge(_devices, left_on=['UserID', 'GroupID'], right_on=['UserID', 'GroupID'], how='left')
    assert all(merged['DeviceID'].notna())
    t = merged['DeviceID'].tolist()
    return t


def allowed_workstations(role: str, _devices):
    general_rol = general_role(role)
    allowed_target_roles = config.login_norms[general_rol]['target workgroups']
    t = _devices[_devices['Role'].isin(allowed_target_roles)]
    return t['DeviceID']


def random_allowed_workstations(sub_logins, _devices):
    for role in sub_logins['Role'].unique():
        role_mask = sub_logins['Role'] == role
        _workstations = allowed_workstations(role, _devices)
        targets = np.random.choice(_workstations, len(sub_logins.loc[role_mask]), replace=True)
        sub_logins.loc[role_mask, 'Target'] = targets
    return sub_logins


def random_servers(size, _devices, server_type: Literal['normal server', 'sensitive server']):
    server_ids = _devices.loc[_devices['Device Type'] == server_type, 'DeviceID']
    t = np.random.choice(server_ids, size)
    return t


def login_targets(_logins, _devices):
    _logins['Target'] = pd.NA
    # _l = _logins['UserID', 'GroupID', 'Role', 'Target Type']
    # roles = _l['Role'].unique()
    # general_roles = [general_role(r) for r in roles]
    targets_types = _logins['Target Type'].unique()
    for target_type in targets_types:
        target_type_mask = _logins['Target Type'] == target_type
        if target_type == 'Self Work Station':
            _logins.loc[target_type_mask, 'Target'] = self_workstation(_logins.loc[target_type_mask],
                                                                       _devices)

        elif target_type == 'other workstations':
            # login target is from allowed_workstations according to privilege or user role.
            _logins.loc[target_type_mask] = random_allowed_workstations(_logins.loc[target_type_mask],
                                                                        _devices)
        elif target_type == 'normal server':
            # target is one normal server
            _logins.loc[target_type_mask, 'Target'] = random_servers(len(_logins.loc[target_type_mask]),
                                                                     _devices, server_type='normal server')

        elif target_type == 'sensitive server':
            # target is one sensitive server
            _logins.loc[target_type_mask, 'Target'] = random_servers(len(_logins.loc[target_type_mask]),
                                                                     _devices, server_type='sensitive server')
        else:
            raise ValueError(target_type)


login_targets(logins, devices)

logins.to_csv('logins.csv', index=False)
