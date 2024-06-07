from typing import List

import pandas as pd
from itertools import combinations


def interval_of_parameters(df, is_not_a_parameter: List = None):
    if is_not_a_parameter is None:  # todo: test
        is_not_a_parameter = ['Login Time']

    parameters = [column for column in df.columns.tolist() if column not in is_not_a_parameter]
    for l in range(1, len(parameters)):
        for parameter_combination in combinations(parameters, l):
            df.sort_values(by=parameter_combination + ['Login Time'], inplace=True)
            df['previous time'] = df['Login Time'].shift(1)
            match_masks = []
            combined_mask = [True] * len(df)
            for parameter in parameter_combination:
                df[f'previous {parameter}'] = df[parameter].shift(1)
                t_mask = (df[f'previous {parameter}'] == df[parameter])
                match_masks += [(df[f'previous {parameter}'] == df[parameter])]
                combined_mask &= t_mask
            df.loc[combined_mask, f'previous {"-".join(parameter_combination)}'] = (
                    df.loc[combined_mask, 'Login Time'] - df.loc[combined_mask, 'previous time']
            )
    return df.sort_values(by='Login Time')
