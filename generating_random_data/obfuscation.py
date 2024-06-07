import numpy as np
import pandas as pd
import config

logins = pd.read_csv("../Data/logins.csv",
                     parse_dates=['Day', 'Shift Start dt', 'Shift End dt', 'Login Time',
                                  'Previous Login Time', ])

logins['UserGroupID'] = logins['UserID'].astype(str) + '-' + logins['GroupID'].astype(str)
logins['DeviceCombineID'] = (logins['Device UserID'].astype(str) + '-' +
                             logins['Device GroupID'].astype(str) + '-' +
                             logins['DeviceID'].astype(str))


# logins = \
#     logins[['UserGroupID', 'Login Time', 'DeviceCombineID']]

def obfuscator(original_field, obfuscated_field, df):
    unique_ids = df[original_field].unique()
    ids_mapped_value = np.random.choice(range(1, len(unique_ids) + 1), len(unique_ids), replace=False)
    maper = {key: value for key, value in zip(unique_ids, ids_mapped_value)}
    df.loc[:, obfuscated_field] = df[original_field].map(maper)


obfuscator('GroupID', 'group', logins)
obfuscator('UserID', 'user', logins)
obfuscator('UserGroupID', 'ip', logins)
obfuscator('DeviceCombineID', 'device', logins)

# unique_users = logins['UserGroupID'].unique()
# unique_users_mapped_value = np.random.choice(range(len(unique_users)), len(unique_users), replace=False)
# unique_user_map = {key: value for key, value in zip(unique_users, unique_users_mapped_value)}
# logins['user'] = logins['UserGroupID'].map(unique_user_map)
#
# unique_devices = logins['DeviceCombineID'].unique()
# unique_devices_mapped_value = np.random.choice(range(len(unique_devices)), len(unique_devices), replace=False)
# unique_devices_map = {key: value for key, value in zip(unique_devices, unique_devices_mapped_value)}
# logins['device'] = logins['DeviceCombineID'].map(unique_devices_map).astype(int)

# logins[['user', 'Login Time', 'device', ]].to_csv('logins.obfuscated.csv', index=False)
# logins[['user', 'Login Time', 'device', ]].to_csv('full-logins.csv', index=False)
logins.to_csv('../Data/logins.obfuscated.full.csv', index=False)
logins[['user', 'group', 'device', 'ip',  'Login Time']].to_csv('../Data/logins.obfuscated.csv', index=False)
