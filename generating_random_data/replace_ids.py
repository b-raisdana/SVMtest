import numpy as np
import pandas as pd

logins = pd.read_csv("logins.csv",
                     parse_dates=['Day', 'Shift Start dt', 'Shift End dt', 'Login Time',
                                          'Previous Login Time', ])

logins['UserGroupID'] = logins['UserID'].astype(str) + '-' + logins['GroupID'].astype(str)
logins['DeviceCombineID'] = (logins['Device UserID'].astype(str) + '-' +
                             logins['Device GroupID'].astype(str) + '-' +
                             logins['DeviceID'].astype(str))

logins = \
    logins[['UserGroupID', 'Login Time', 'DeviceCombineID']]

unique_users = logins['UserGroupID'].unique()
unique_users_mapped_value = np.random.choice(range(len(unique_users)), len(unique_users), replace=False)
unique_user_map = {key: value for key, value in zip(unique_users, unique_users_mapped_value)}
logins['user'] = logins['UserGroupID'].map(unique_user_map)

unique_devices = logins['DeviceCombineID'].unique()
unique_devices_mapped_value = np.random.choice(range(len(unique_devices)), len(unique_devices), replace=False)
unique_devices_map = {key: value for key, value in zip(unique_devices, unique_devices_mapped_value)}
logins['device'] = logins['DeviceCombineID'].map(unique_devices_map).astype(int)

logins[['user', 'Login Time', 'device', ]].to_csv('obfuscated-login.csv', index=False)
logins[['user', 'Login Time', 'device', ]].to_csv('full-login.csv', index=False)
