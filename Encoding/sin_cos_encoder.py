import numpy as np


def sin_cos_encoder(values: np.ndarray[float], max_value: float) -> np.ndarray:
    """
    Encode a given parameter as sin and cos values.

    Args:
    values (np.ndarray[float]): The ndarray of raw values.
    max_value (float): The max value of parameter.

    Returns:
    tuple: A tuple containing the sine and cosine encoding of the hour.
    """
    angle = values * 2 * np.pi / max_value
    sin_enc = np.sin(angle)
    cos_enc = np.cos(angle)
    return sin_enc, cos_enc
