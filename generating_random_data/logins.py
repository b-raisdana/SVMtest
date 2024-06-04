import datetime

import numpy as np
import pandas as pd

from generating_random_data import config

daily_timesheet = pd.read_csv("shift_employees.csv", parse_dates=['Day'])


def first_login(_daily_timesheet):
    _logins = _daily_timesheet.copy()
    _logins['Type'] = 'Self Work Station'
    _logins['Login Target'] = _logins[['UserID', 'GroupID', 'Type']].to_records(index=False)
    not_first_logins_idxs = np.random.choice(_daily_timesheet.index,
                                             len(_daily_timesheet) * (1 - config.self_workstation_first_login_rate),
                                             replace=False)
    _logins.drop(not_first_logins_idxs, axis='indexes')
    return _logins


logins = first_login(daily_timesheet)


def drop_near_re_logins(_logins):
    sorted_daily_timesheet = _logins.sort_values(by=['Day', 'UserID', 'Login Time'], ascending=True).copy()
    sorted_daily_timesheet['Previous Login UserID'] = sorted_daily_timesheet['UserID'].shift(-1)
    sorted_daily_timesheet['Previous Login Time'] = sorted_daily_timesheet['Login Time'].shift(-1)
    near_logins_idxs = sorted_daily_timesheet.iloc[1:][
        (sorted_daily_timesheet['UserID'] == sorted_daily_timesheet['Previous Login UserID']) &
        ((sorted_daily_timesheet['Login Time'] - sorted_daily_timesheet['Previous Login Time']) <
         datetime.timedelta(minutes=config.min_inter_login_mins))
        ].index
    _logins.drop(near_logins_idxs, axis='indexes')


def more_login_to_self_workstations(_daily_timesheet: pd.DataFrame, _logins: pd.DataFrame):
    re_logi_idxs = np.random.choice(_logins.index, len(_daily_timesheet) * config.self_workstation_next_login_rate,
                                    replace=True)
    re_logins: pd.DataFrame = _logins.iloc[re_logi_idxs].copy()
    re_logins['Login Time'] = pd.Timestamp.fromtimestamp(
        np.random.randint(re_logins['Shift Start'].to_datetime().total_seconds(),
                          re_logins['Shift End'].to_datetime().total_seconds()))
    _logins = pd.concat([logins, re_logins])
    drop_near_re_logins(_logins)
    # for re_login in re_logins.index:
    #     last_login_of_same_user = _logins.loc[(
    #             (_logins['Day'] == re_logins.loc[re_login, 'Day']) &
    #             (_logins['UserID'] == re_logins.loc[re_login, 'UserID'])
    #     )].sort_by('Login Time').last()
    #     new_login_time = datetime.fromtimestamp(random.randint(
    #         (last_login_of_same_user['Login Time'] + config.min_inter_login_mins).to_datetime().total_seconds(),
    #         last_login_of_same_user['Shift End'].to_datetime().total_seconds()))
    #     re_logins.loc[re_login, 'Login Time'] = new_login_time
    #     _logins = pd.concat(logins, re_logins.loc[re_login])


more_login_to_self_workstations(daily_timesheet, logins)


def logins_to_other_device(_daily_timesheet: pd.DataFrame, _logins: pd.DataFrame):
    for user_type, user_parameters in config.login_norms.items():
        roles: list = user_parameters['roles']
        rates: dict = user_parameters['rates']

        user_type_timeshift_idx = _daily_timesheet[_daily_timesheet['Role'].isin(roles)].index
        for device_type, device_parameters in rates.items():
            proportion = device_parameters['proportion']
            _max = device_parameters['max']
            idxs_for_logins_to_device_type = \
                np.random.choice(user_type_timeshift_idx, round(len(user_type_timeshift_idx) * proportion))
            user_type_timeshift_idx_repeat = np.random.randint(0, _max, len(idxs_for_logins_to_device_type))
            # [item for item, count in zip(list1, list2) for _ in range(count)]
            duplicated_ids_for_logins = \
                [idx for idx, count in zip(idxs_for_logins_to_device_type, user_type_timeshift_idx_repeat)
                 for _ in range(count)]
            new_logins = _daily_timesheet.loc[duplicated_ids_for_logins].copy()
            new_logins['Login Time'] = pd.Timestamp.fromtimestamp(
                np.random.randint(new_logins['Shift Start'].to_datetime().total_seconds(),
                                  new_logins['Shift End'].to_datetime().total_seconds()))
            _logins = pd.concat([_logins, new_logins])

    drop_near_re_logins(_logins)


logins_to_other_device(daily_timesheet, logins)
