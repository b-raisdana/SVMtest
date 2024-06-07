from itertools import combinations

import pandas as pd


def frequency_by_parameter(df: pd.DataFrame, timeframes, non_parameter_columns=None):
    """
    Types of frequency calculations:
    -single parameter
    -parameter combination
    """
    if non_parameter_columns is None:  # todo: test
        non_parameter_columns = ['Login Time']
    parameters = [parameter for parameter in df.columns if parameter not in non_parameter_columns]

    frequency_df = pd.DataFrame(index=pd.MultiIndex.from_product(
        [[], []], names=['field_name', 'timeframe']))
    for r in range(1, len(parameters) + 1):
        parameter_combinations = combinations(parameters, r)
        for combination in parameter_combinations:
            for timeframe in timeframes:
                df.set_index('Login Time', inplace=True)
                frequency_df.loc[f"-".join(combination), timeframe] = \
                    df.groupby(combination).resample(timeframe).count()

    return frequency_df
