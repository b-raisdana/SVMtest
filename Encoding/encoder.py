import pandas as pd

from Encoding.sin_cos_encoder import sin_cos_encoder

data = pd.read_csv('../Data/logins.obfuscated.pre_processed.csv', parse_dates=['Login Time'])


def encode(df: pd.DataFrame) -> pd.DataFrame:
    df['encoded day of week'] = sin_cos_encoder(df['Login Time'].dt.weekday, 6)
    df['encoded day of month'] = sin_cos_encoder(df['Login Time'].dt.day / df['Login Time'].dt.days_in_month, 1)
    df['encoded time of day'] = sin_cos_encoder(df['Login Time'].dt.hour + df['Login Time'].dt.minute / 60, 24)
    return df


data.to_csv('../Data/logins.obfuscated.encoded.csv', index=False)
