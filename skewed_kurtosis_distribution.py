import scipy
import plotly.graph_objects as go
import numpy as np
from random import random

distribution = scipy.stats.gengamma(300, 0.1, loc=50, scale=1)
pre_samples = distribution.rvs(size=100000)  # Generate 1000 random samples
min = pre_samples.min() - random()*2
max = pre_samples.max() + random()*2
# Apply CDF transfo
# rmation to map samples to the range [0, 24]
cdf_values = distribution.cdf(pre_samples)  # Map to [0, 1]
samples = cdf_values * 24  # Scale to [0, 24]
samples = (pre_samples - min) / (max - min) * 24
# Create a histogram of the samples
histogram = go.Histogram(x=samples, nbinsx=200, name='Samples', opacity=0.75)
fig = go.Figure(data=[histogram])
fig.update_layout(
    title='Generalized Gamma Distribution', xaxis_title='Value', yaxis_title='Frequency', barmode='overlay'
)
# Show the plot
fig.show()
