from itertools import combinations

import pandas as pd

data = pd.read_csv("../Data/logins.obfuscated.csv", parse_dates=['Login Time'])


def frequency_by_parameter(df: pd.DataFrame, timeframes, non_parameter_columns=None):
    """
    Types of frequency calculations:
    -single parameter
    -parameter combination
    """
    if non_parameter_columns is None:  # todo: test
        non_parameter_columns = ['Login Time']
    parameters = [parameter for parameter in df.columns if parameter not in non_parameter_columns]

    # frequency_df = pd.DataFrame(index=pd.MultiIndex.from_product(
    #     [[], []], names=['field_name', 'timeframe']))
    frequency_df = pd.DataFrame()
    df.set_index('Login Time', inplace=True)
    for r in range(1, len(parameters) + 1):
        parameter_combinations = combinations(parameters, r)
        for combination in parameter_combinations:
            for timeframe in timeframes:
                # if r == 2:
                #     nop = 1
                # t = df.groupby(list(combination)).resample(timeframe).count()#.rename(columns={combination})
                t = df.groupby(list(combination)).resample(timeframe).size().reset_index(name='count')
                t['timeframe'] = timeframe
                # t.reset_index(inplace=True)
                t.set_index(['timeframe', 'Login Time'], inplace=True)
                frequency_df = pd.concat([frequency_df, t])
                # frequency_df.loc[f"-".join(combination), timeframe] = \
                #     df.groupby(list(combination)).resample(timeframe).count()
    df.reset_index()

    return frequency_df


def frequency_processor(df: pd.DataFrame) -> pd.DataFrame:
    frequency_df = frequency_by_parameter(df, ['1W', '1d', '1h', '15min'])
    return frequency_df


frequency_data = frequency_processor(data)
frequency_data.to_csv('../Data/logins.frequency.csv', index=False)
