from itertools import combinations

import pandas as pd


def frequency_by_parameter(df: pd.DataFrame, timeframes, non_parameter_columns=None):
    """
    Types of frequency calculations:
    -single parameter
    -parameter combination
    """
    if non_parameter_columns is None:
        non_parameter_columns = ['Login Time']
    parameters = [parameter for parameter in df.columns if parameter not in non_parameter_columns]
    frequency_df = pd.DataFrame()
    for r in range(1, len(parameters) + 1):
        parameter_combinations = combinations(parameters, r)
        for combination in parameter_combinations:
            for timeframe in timeframes:
                """
                Example:
                group by ['user', 'device'] for 15min frequency.
                Sample data:
                user,group,device,ip,Login Time
                129,9,144,15,2023-01-01 09:41:03.060907002
                129,9,144,15,2023-01-02 08:08:59.805345360
                129,9,164,15,2023-01-02 12:00:32.443895183
                129,9,143,15,2023-01-02 12:12:38.139441302
                129,9,69,15,2023-01-02 13:45:20.909711558
                129,9,38,15,2023-01-02 14:48:21.227305631
                """
                df.set_index('Login Time', inplace=True)
                frequency_df[f'frequecy {"-".join(combination)} {timeframe}'] = \
                    df.groupby(combination).resample(timeframe).count()

    return frequency_df
