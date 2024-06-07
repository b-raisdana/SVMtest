import pandas as pd

from Preprocessing.parameter_timeframe_count import inter_activity_time_by_parameter
from Preprocessing.pramater_frequency import frequency_by_parameter

data = pd.read_csv("../logins.obfuscated.csv", pare_date=['Login Time'])


def pre_processor(df: pd.DataFrame) -> pd.DataFrame:
    df = inter_activity_time_by_parameter(df)
    frequency_df = frequency_by_parameter(df, ['1w', '1d', '1h', '15min'])
    return frequency_df


frequency_data = pre_processor(data)

frequency_data.to_csv('../logins.obfuscated.pre_processed.csv', index=False)
