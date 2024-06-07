import os
import sys

import pandas as pd

from Preprocessing.interval_of_parameters import interval_of_parameters
from Preprocessing.pramater_frequency import frequency_by_parameter

cwd = os.getcwd()
# print(cwd)
# exit()
# sys.exit()

data = pd.read_csv("../Data/logins.obfuscated.csv", parse_dates=['Login Time'])


def pre_record_processor(df: pd.DataFrame) -> pd.DataFrame:
    df = interval_of_parameters(df)
    return df


data = pre_record_processor(data)  # todo: test
data.to_csv("../Data/logins.pre_processed.csv", index=False)


def frequency_processor(df: pd.DataFrame) -> pd.DataFrame:
    frequency_df = frequency_by_parameter(df, ['1w', '1d', '1h', '15min'])
    return frequency_df


frequency_data = frequency_processor(data)
frequency_data.to_csv('../Data/logins.frequency.csv', index=False)
