"""
This is my sample data:
user,group,device,ip,Login Time
129,9,144,15,2023-01-01 09:41:03.060907002
129,9,144,15,2023-01-02 08:08:59.805345360
129,9,164,15,2023-01-02 12:00:32.443895183
129,9,143,15,2023-01-02 12:12:38.139441302
129,9,69,15,2023-01-02 13:45:20.909711558
I want to generate the IQR of number of logins for each user according to 1t's maximum of 2 week previous data.
"""


To calculate the interquartile range (IQR) of the number of logins for each user based on the maximum of 2 weeks of previous data, we can follow these steps:

1. **Read the data**: Parse the provided data into a suitable format, like a DataFrame.
2. **Preprocess the data**: Convert the "Login Time" column to datetime format.
3. **Group the data**: Group by user and within each group, create a rolling window of 2 weeks to count the logins.
4. **Calculate the IQR**: For each user, compute the IQR of the number of logins within the 2-week windows.

Let's implement this step-by-step using Python with the help of pandas.

```python
import pandas as pd

# Sample data
data = {
    'user': [129, 129, 129, 129, 129],
    'group': [9, 9, 9, 9, 9],
    'device': [144, 144, 164, 143, 69],
    'ip': [15, 15, 15, 15, 15],
    'Login Time': [
        "2023-01-01 09:41:03.060907002",
        "2023-01-02 08:08:59.805345360",
        "2023-01-02 12:00:32.443895183",
        "2023-01-02 12:12:38.139441302",
        "2023-01-02 13:45:20.909711558"
    ]
}

# Create DataFrame
df = pd.DataFrame(data)

# Convert 'Login Time' to datetime
df['Login Time'] = pd.to_datetime(df['Login Time'])

# Sort by user and 'Login Time'
df = df.sort_values(by=['user', 'Login Time'])

# Function to calculate the number of logins in the past 2 weeks for each login
def count_logins_in_last_2_weeks(df):
    df['Login Count'] = df['Login Time'].apply(
        lambda x: df[(df['Login Time'] <= x) & (df['Login Time'] > (x - pd.Timedelta(weeks=2)))].shape[0]
    )
    return df

# Apply the function to each user group
df = df.groupby('user').apply(count_logins_in_last_2_weeks)

# Calculate IQR of login counts for each user
def calculate_iqr(series):
    return series.quantile(0.75) - series.quantile(0.25)

iqr_per_user = df.groupby('user')['Login Count'].apply(calculate_iqr)

iqr_per_user
'''
### Explanation
1. **Sample Data**: We first create a dictionary with the sample data and convert it into a pandas DataFrame.
2. **Convert Login Time**: Convert the "Login Time" column to a datetime object for easier manipulation.
3. **Sort Data**: Sort the data by user and login time to ensure proper chronological order.
4. **Rolling Count**: Define a function `count_logins_in_last_2_weeks` to count the number of logins in the past 2 weeks for each login time.
5. **Apply Function**: Apply this function to each user group using `groupby`.
6. **Calculate IQR**: Calculate the IQR for the 'Login Count' for each user using the quantile method.

This code will output the IQR of the number of logins for each user over rolling 2-week windows.
'''