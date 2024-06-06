import numpy as np


def encode_time(day):
    """
    Encode a given hour (0-23) as sin and cos values.

    Args:
    hour (int): The hour of the day (0-23).

    Returns:
    tuple: A tuple containing the sine and cosine encoding of the hour.
    """
    angle = day * 2 * np.pi / 30
    sin_time = np.sin(angle)
    cos_time = np.cos(angle)
    return sin_time, cos_time


# Example usage:
hour = 15  # 3 PM
sin_time, cos_time = encode_time(hour)
print(f"Hour: {hour}, Sin: {sin_time}, Cos: {cos_time}")