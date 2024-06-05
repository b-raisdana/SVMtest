import numpy as np
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots

'''
This is the format of my logins.csv:
UserID,GroupID,Role,Day,ShiftID,Shift,Shift Start H,Shift End H,Shift Start dt,Shift End dt,Target Type,Login Time,Login Seconds Shifter,Previous UserID,Previous Login Time,Target
0,1,Admin,2023-01-01,0.0,day,8.0,17.0,2023-01-01 08:00:00,2023-01-01 17:00:00,Self Work Station,2023-01-01 09:41:03.060907002,,,,0
0,1,Admin,2023-01-02,0.0,day,8.0,17.0,2023-01-02 08:00:00,2023-01-02 17:00:00,Self Work Station,2023-01-02 08:08:59.805345360,,0.0,2023-01-01 09:41:03.060907002,0
<br>
in plotly: creat a subplot for each role:['Regular Day', 'Regular Shift', 'Support Shift', 'Support Day', 'Admin', ], dedicate a vertical offset to each user, for each login, draw a filled circle colored by the color assigned to use with diameter of 2 pixels. this circle should be premitted by another shape as below:
-if Device Type is 'workstation': an empty circle with 4 pixels diameter colored by unique colors for devices, which are less than 255
-if Device Type is 'normal server': an empty triangle with 5 pixels diameter colored by unique colors for devices, which are less than 255
-if Device Type is 'sensitive server': an empty square with 6 pixels diameter colored by unique colors for devices, which are less than 255
'''

logins = pd.read_csv('logins.csv',
                     parse_dates=['Day', 'Shift Start dt', 'Shift End dt', 'Login Time', 'Previous Login Time', ])
roles = ['Regular Day', 'Regular Shift', 'Support Shift', 'Support Day', 'Admin']
device_shapes = {
    'workstation': {'symbol': 'circle-open', 'size': 6},
    'normal server': {'symbol': 'triangle-up-open', 'size': 8},
    'sensitive server': {'symbol': 'square-open', 'size': 10}
}


def color_of(user_id, device_id=None):
    if not np.isnan(user_id):
        return f'hsl({user_id % 255}, 100%, 50%)'
    else:
        return f'hsl({device_id % 255}, 100%, 50%)'


fig = make_subplots(rows=len(roles), cols=1, shared_xaxes=True, subplot_titles=roles)

for i, role in enumerate(roles):
    role_data = logins[logins['Role'] == role]
    role_color = color_of(i * 5)
    for j, user in enumerate(role_data['UserID'].unique()):
        user_data = role_data[role_data['UserID'] == user]
        user_color = color_of(user)
        for device_type in user_data['Device Type'].unique():
            user_device_type_data = user_data.loc[user_data['Device Type']==device_type]
            device_shape = device_shapes[device_type]
            user_device_login_times = user_device_type_data['Login Time']
            y_coordinates = [j * 10] * len(user_device_login_times)
            # device_markers = user_data['Device Type'].map(device_shapes)
            device_color = user_device_type_data.apply(lambda row: color_of(row['Device UserID'], row['DeviceID']), axis=1)
            fig.add_trace(go.Scatter(
                x=user_device_login_times,
                y=y_coordinates,
                mode='markers',
                marker=dict(color=user_color, size=2),
                showlegend=False
            ), row=i + 1, col=1)
            fig.add_trace(go.Scatter(
                x=user_device_login_times,
                y=y_coordinates,
                mode='markers',
                marker=dict(color=role_color, size=4),
                showlegend=False
            ), row=i + 1, col=1)
            fig.add_trace(go.Scatter(
                x=user_device_login_times,
                y=y_coordinates,
                mode='markers',
                marker=device_shape,
                showlegend=False
            ), row=i + 1, col=1)
        # for _, row in user_data.iterrows():
        #     # Plot filled circle for each login
        #     fig.add_trace(go.Scatter(
        #         x=[row['Login Time']],
        #         y=[j * 10],  # Vertical offset for each role
        #         mode='markers',
        #         marker=dict(color=user_color, size=2),
        #         showlegend=False
        #     ), row=i + 1, col=1)
        #
        #     fig.add_trace(go.Scatter(
        #         x=[row['Login Time']],
        #         y=[j * 10],  # Vertical offset for each role
        #         mode='markers',
        #         marker=dict(color=role_color, size=4),
        #         showlegend=False
        #     ), row=i + 1, col=1)
        #
        #     # Plot additional shapes based on device type
        #     if row['Device Type'] in device_shapes:
        #         shape = device_shapes[row['Device Type']]
        #         if not np.isnan(row['Device UserID']):
        #             device_color = color_of(row['Device UserID'])
        #         else:
        #             device_color = color_of(row['DeviceID'])
        #         fig.add_trace(go.Scatter(
        #             x=[row['Login Time']],
        #             y=[j * 10],  # Vertical offset for each role
        #             mode='markers',
        #             marker=dict(symbol=shape['symbol'], size=shape['size'], color=device_color),
        #             showlegend=False
        #         ), row=i + 1, col=1)
        #     else:
        #         raise ValueError(row['Device Type'])

# Update layout
fig.update_layout(
    height=800,
    title_text='Logins by Role',
    xaxis_title='Login Time',
    yaxis_title='Role',
    showlegend=False
)

# Update y-axes labels
for i, role in enumerate(roles):
    fig.update_yaxes(title_text=role, row=i + 1, col=1)

# Show plot
fig.show()
