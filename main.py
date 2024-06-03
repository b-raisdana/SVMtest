import datetime

import pandas as pd
import plotly.graph_objects as go
import numpy as np
import time

timeframe = '15min'
window_size = datetime.timedelta(hours=4)
log_df = pd.read_csv("./2024_06_02 12_29_20.csv", parse_dates=['recvTime'])
min_time = pd.to_datetime(log_df['recvTime'].min()).floor(timeframe)
max_time = pd.to_datetime(log_df['recvTime'].max()).ceil(timeframe)
time_range = pd.date_range(start=min_time, end=max_time, freq=timeframe)
dest_ip_addresses = log_df['destIpAddr'].unique()
ip_time_combinations = pd.MultiIndex.from_product([dest_ip_addresses, time_range], names=['destIpAddr', 'recvTime'])
ip_time_df = pd.DataFrame(index=ip_time_combinations).reset_index()
# fig1 = go.Figure()
# for i, ip in enumerate(dest_ip_addresses):
#     per_ip_logs = log_df[log_df['destIpAddr'] == dest_ip_addresses[i]]
#     color = f'hsl({i * (360 / len(dest_ip_addresses))}, 50%, 50%)'
#     fig1.add_scatter(
#         x=log_df['recvTime'],
#         y=[i * 10 + 1] * len(per_ip_logs),
#         mode='markers',
#         marker=dict(
#             symbol='circle',
#             size=10,
#             color=color,
#             line=dict(width=0)
#         ),
#         name=f'{ip}'
#     )
# fig1.show()

grouped_logs = log_df.groupby(['destIpAddr', pd.Grouper(key='recvTime', freq=timeframe)]).size().reset_index(
    name='log_count').set_index(['destIpAddr', 'recvTime'])
grouped_logs = ip_time_df.merge(grouped_logs, on=['destIpAddr', 'recvTime'], how='left').fillna(0).set_index(
    ['destIpAddr', 'recvTime'])
fig2 = go.Figure()

# t = [1,2,3,4,5,65,6,7]
# df1 = pd.DataFrame(t, columns=['data1'])
# np = 1
# dest_ip_addresses = ['192.168.167.19']
iter_counter = 0
for i, ip in enumerate(dest_ip_addresses):
    """
    calculate IQR for each IP for each recvTime based in previous 120 minutes
    """
    per_ip_log_indexes = grouped_logs[grouped_logs.index.get_level_values('destIpAddr') == dest_ip_addresses[i]].index
    # grouped_logs.loc[per_ip_log_indexes, 'lower_band'] = grouped_logs.loc[per_ip_log_indexes,'log_count'].sort_values(ascending=True).quantile(0.25)
    # grouped_logs.loc[per_ip_log_indexes, 'upper_band'] = grouped_logs.loc[per_ip_log_indexes,'log_count'].sort_values(ascending=True).quantile(0.75)

    # Calculate the IQR for each recvTime based on the previous 120 minutes
    for window_end in pd.date_range(start=min_time + window_size, end=max_time, freq=timeframe):
        window_start = window_end - window_size
        window_indexes = grouped_logs[(
                (grouped_logs.index.get_level_values('destIpAddr') == dest_ip_addresses[i]) &
                (grouped_logs.index.get_level_values('recvTime') > window_start) &
                (grouped_logs.index.get_level_values('recvTime') < window_end)
        )].index
        window = grouped_logs.loc[window_indexes]
        grouped_logs.loc[(
                (grouped_logs.index.get_level_values('destIpAddr') == dest_ip_addresses[i]) &
                (grouped_logs.index.get_level_values('recvTime') == window_end)
        ), 'lower_band'] = window['log_count'].quantile(0.5)
        grouped_logs.loc[(
                (grouped_logs.index.get_level_values('destIpAddr') == dest_ip_addresses[i]) &
                (grouped_logs.index.get_level_values('recvTime') == window_end)
        ), 'upper_band'] = window['log_count'].quantile(0.95)
        if iter_counter % 1000 == 0:
            print(f"iter:{iter_counter}")
        iter_counter += 1

    # for idx in per_ip_log_indexes.get_level_values('recvTime'):
    #     window_start = idx[1] - pd.Timedelta(minutes=120)
    #     window_end = idx[1]
    #
    #     # Filter the logs for the current IP address within the rolling window
    #     windows_indexes = grouped_logs[(
    #         (grouped_logs.index.get_level_values('destIpAddr')== dest_ip_addresses[i]) &
    #         (grouped_logs.index.get_level_values('recvTime') > window_start) &
    #         (grouped_logs.index.get_level_values('recvTime') < window_end)
    #     )].index
    #     logs_within_window = grouped_logs.loc[per_ip_log_indexes &
    #                                           (per_ip_log_indexes.get_level_values('recvTime') < window_end) &
    #                                           (per_ip_log_indexes.get_level_values('recvTime') > window_start)]
    #
    #                                           slice(window_start, window_end)), 'log_count']
    #
    #     # Calculate the lower and upper quartiles for the current window
    #     lower_band = logs_within_window.quantile(0.25)
    #     upper_band = logs_within_window.quantile(0.75)
    #
    #     # Assign the calculated lower and upper quartiles to the DataFrame
    #     grouped_logs.loc[idx, 'lower_band'] = lower_band
    #     grouped_logs.loc[idx, 'upper_band'] = upper_band

for i, ip in enumerate(dest_ip_addresses):
    per_ip_logs = grouped_logs[grouped_logs.index.get_level_values('destIpAddr') == dest_ip_addresses[i]]
    color = f'hsl({i * (360 / len(dest_ip_addresses))}, 50%, 50%)'
    fig2.add_trace(go.Scatter(
        x=per_ip_logs.index.get_level_values(level='recvTime'),
        y=per_ip_logs['log_count'],
        mode='lines',
        line=dict(color=color, width=1),
        name=f'IP {ip}'
    ))
    fig2.add_trace(go.Scatter(
        x=per_ip_logs.index.get_level_values(level='recvTime'),
        y=per_ip_logs['lower_band'],
        mode='lines',
        line=dict(color=color, width=2),
        name=f'IP {ip}'
    ))
    fig2.add_trace(go.Scatter(
        x=per_ip_logs.index.get_level_values(level='recvTime'),
        y=per_ip_logs['upper_band'],
        mode='lines',
        line=dict(color=color, width=2),
        name=f'IP {ip}'
    ))
    # Calculate IQR
    # q1 = per_ip_logs['log_count'].quantile(0.25)
    # q3 = per_ip_logs['log_count'].quantile(0.75)
    # iqr = q3 - q1

    # Add IQR range as a shape

    # fig2.add_shape(
    #     type='rect',
    #     x0=per_ip_logs['recvTime'].iloc[0],
    #     y0=lower_band,
    #     x1=per_ip_logs['recvTime'].iloc[-1],
    #     y1=q3,
    #     line=dict(color=color),
    #     fillcolor=color,
    #     opacity=0.3,
    #     name=f'IQR for IP {ip}'
    # )

fig2.show()
nop = 1
