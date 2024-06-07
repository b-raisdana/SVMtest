from typing import List

import numpy as np
import pandas as pd
from itertools import combinations


def interval_of_parameters(df, is_not_a_parameter: List = None):
    if is_not_a_parameter is None:  # todo: test
        is_not_a_parameter = ['Login Time']

    parameters = [column for column in df.columns.tolist() if column not in is_not_a_parameter]
    for l in range(1, len(parameters)):
        for parameter_combination in combinations(parameters, l):
            df.sort_values(by=list(parameter_combination) + ['Login Time'], inplace=True)
            df['previous time'] = df['Login Time'].shift(1)
            # match_masks = []
            combined_mask = pd.Series([True] * len(df)).astype(bool)
            for parameter in parameter_combination:
                df[f'previous {parameter}'] = df[parameter].shift(1)
                t_mask = (df[f'previous {parameter}'] == df[parameter])
                # match_masks += [(df[f'previous {parameter}'] == df[parameter])]
                combined_mask &= t_mask
            df.loc[combined_mask, f'timedelta to previous same {"-".join(parameter_combination)}'] = (
                    df.loc[combined_mask, 'Login Time'] - df.loc[combined_mask, 'previous time']
            ).dt.total_seconds().astype(np.float32)
            df.drop(columns=[f'previous {parameter}' for parameter in parameter_combination] + ['previous time'],
                    inplace=True)
    return df.sort_values(by='Login Time')

data = pd.read_csv("../Data/logins.obfuscated.csv", parse_dates=['Login Time'])


def pre_record_processor(df: pd.DataFrame) -> pd.DataFrame:
    df = interval_of_parameters(df)
    return df


data = pre_record_processor(data)  # todo: test
data.to_csv("../Data/logins.pre_processed.interval_of_parameters.csv", index=False)