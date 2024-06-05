import pandas as pd


def pre_process_inter_login():
    df = pd.read_csv('obfuscated-login.csv', parse_dates=['Login Time'])

    # Convert 'Login Time' to timestamp in seconds
    df['Login Time'] = (df['Login Time'] - pd.Timestamp("1970-01-01")) // pd.Timedelta('1s')

    df.sort_values(by=['user', 'Login Time'], inplace=True)
    # df.reset_index(drop = True)
    df['Previous user'] = df['user'].shift(1)
    df['Previous user Login'] = df['Login Time'].shift(1)
    df.loc[(df['Previous user'] != df['user']), 'Previous user Login'] = pd.NA
    df.drop(columns='Previous user', axis='columns', inplace=True)
    df.drop(df[df['Previous user Login'].isna()].index, axis='rows', inplace=True)
    df['user inter login time'] = df['Login Time'] - df['Previous user Login']

    df.sort_values(by=['device', 'Login Time'], inplace=True)
    # df.reset_index(drop = True)
    df['Previous device'] = df['device'].shift(1)
    df['Previous device Login'] = df['Login Time'].shift(1)
    df.loc[(df['Previous device'] != df['device']), 'Previous device Login'] = pd.NA
    df.drop(columns='Previous device', axis='columns', inplace=True)
    df.drop(df[df['Previous device Login'].isna()].index, axis='rows', inplace=True)
    df['device inter login time'] = df['Login Time'] - df['Previous device Login']

    return df