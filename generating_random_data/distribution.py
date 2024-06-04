import numpy as np
import plotly.graph_objs as go
import scipy

from generating_random_data import config


# distribution = scipy.stats.gengamma(300, 0.1, loc=50, scale=1)
# pre_samples = distribution.rvs(size=10000)  # Generate 1000 random samples
# min = pre_samples.min() - random()*2
# max = pre_samples.max() + random()*2
# # Apply CDF transfo
# # rmation to map samples to the range [0, 24]
# cdf_values = distribution.cdf(pre_samples)  # Map to [0, 1]
# samples = cdf_values * 24  # Scale to [0, 24]
# samples = (pre_samples - min) / (max - min) * 24
# # Create a histogram of the samples
# histogram = go.Histogram(x=samples, nbinsx=200, name='Samples', opacity=0.75)
# fig = go.Figure(data=[histogram])
# fig.update_layout(
#     title='Generalized Gamma Distribution', xaxis_title='Value', yaxis_title='Frequency', barmode='overlay'
# )
# # Show the plot
# fig.show()

def gaussian_distribution1(start, end, mean, std, skew, kurt, size=1000):
    # Generate base Gaussian distribution
    base_gaussian = np.random.normal(loc=mean, scale=std, size=size)

    # Adjust for skewness and kurtosis using Johnson's SU distribution
    gamma, xi, loc, scale = scipy.stats.johnsonsu.fit(base_gaussian)
    transformed_data = scipy.stats.johnsonsu.rvs(gamma, xi, loc=loc, scale=scale, size=size)

    # Shift the distribution to have the desired mean and std
    transformed_data = (transformed_data - np.mean(transformed_data)) / np.std(transformed_data) * std + mean

    # Truncate data to be within [start, end]
    transformed_data = np.clip(transformed_data, start, end)

    return transformed_data


def gaussian2(start, end, skew, kurt, size=1000):
    mean = np.average([start, end])
    std = (end - start) / 4
    # Generate base Gaussian distribution
    base_gaussian = np.random.normal(loc=mean, scale=std, size=size)

    # Adjust for skewness and kurtosis using Johnson's SU distribution
    gamma, xi, loc, scale = scipy.stats.johnsonsu.fit(base_gaussian)
    transformed_data = scipy.stats.johnsonsu.rvs(gamma, xi, loc=loc, scale=scale, size=size)

    # Shift the distribution to have the desired mean and std
    transformed_data = (transformed_data - np.mean(transformed_data)) / np.std(transformed_data) * std + mean

    # Ensure skewness and kurtosis are close to desired values
    skewed_data = scipy.stats.skewnorm.rvs(a=skew, loc=mean, scale=std, size=size)
    fitted_data = scipy.stats.johnsonsu.fit(skewed_data)
    adjusted_data = scipy.stats.johnsonsu.rvs(*fitted_data, size=size)
    transformed_data = np.clip(adjusted_data, start, end)

    return transformed_data


def gaussian3(start, end, skew=0, kurt=3, size=1000, tol=0.01, max_iter=1000, fit=True):
    mean = np.average([start, end])
    std = (end - start) / 4

    # Helper function to compute skewness and kurtosis of a distribution
    def compute_skew_kurt(data):
        return scipy.stats.skew(data), scipy.stats.kurtosis(data, fisher=True)

    # Generate initial base Gaussian distribution
    base_gaussian = np.random.normal(loc=mean, scale=std, size=size)

    # Iteratively adjust Johnson SU parameters to match desired skewness and kurtosis
    gamma, xi, loc, scale = scipy.stats.johnsonsu.fit(base_gaussian)
    for i in range(max_iter):
        samples = scipy.stats.johnsonsu.rvs(gamma, xi, loc=loc, scale=scale, size=size)

        # Normalize data to have the desired mean and std
        samples = (samples - np.mean(samples)) / np.std(samples) * std + mean

        # Compute current skewness and kurtosis
        current_skew, current_kurt = compute_skew_kurt(samples)

        # Check if the current skewness and kurtosis are within tolerance
        if (abs(current_skew - skew) < tol) and (abs(current_kurt - kurt) < tol):
            break

        # Adjust Johnson SU parameters based on the difference
        gamma += (skew - current_skew) * (1 / max_iter)
        xi += (kurt - current_kurt) * (1 / max_iter)

    # Clip data to be within [start, end]
    if fit:
        # samples = np.clip(samples, start, end)
        samples = samples[(samples >= start) & (samples <= end)]

    return samples


_start = -30
_end = 150


def normal(start, end, size, fit=False):
    if fit:
        while True:
            _samples = np.random.normal(np.average([start, end]), (end - start) / 4, int(size * 1.2))
            _samples = _samples[(_samples > start) & (_samples < end)]
            if len(_samples) > size:
                return _samples[:size]
    else:
        return np.random.normal(np.average([start, end]), (end - start) / 2, int(size))


def gaussian(start, end, size, skew=0.0):
    mean = np.average([start, end])
    std = (end - start) / 2
    sigma = skew / np.sqrt(1.0 + skew ** 2)
    u0 = np.random.randn(size)
    v = np.random.randn(size)
    u1 = (sigma * u0 + np.sqrt(1.0 - sigma ** 2) * v) * std
    u1[u0 < 0] *= -1
    u1 = u1 + mean
    return u1


# # samples = normal(_start, _end, 10000)
# # samples = gaussian(start=_start, end=_end, size=700, skew=-10)
# samples = gaussian(start=-config.normal_early_start_mins, end=config.normal_late_start_mins,
#                                     size=6200, skew=4)
# # pre_samples = distribution.rvs(size=10000)  # Generate 1000 random samples
# # min = pre_samples.min() - random()*2
# # max = pre_samples.max() + random()*2
# # # Apply CDF transfo
# # # rmation to map samples to the range [0, 24]
# # cdf_values = distribution.cdf(pre_samples)  # Map to [0, 1]
# # samples = cdf_values * 24  # Scale to [0, 24]
# # samples = (pre_samples - min) / (max - min) * 24
# # Create a histogram of the samples
# histogram = go.Histogram(x=samples, nbinsx=200, name='Samples', opacity=0.75)
# fig = go.Figure(data=[histogram])
# fig.update_layout(
#     title='Generalized Gamma Distribution', xaxis_title='Value', yaxis_title='Frequency', barmode='overlay'
# )
# # Show the plot
# fig.show()
