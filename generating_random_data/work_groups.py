from typing import List

import numpy as np
import pandas as pd

from generating_random_data.config import num_groups, total_employees, roles, min_groups_for_roles, role_distribution, \
    role_distribution_tolerance

"""
•	10 work groups including 150 users in total
•	Duration Range of Data: 6 weeks
	User role Distribution:
•	3% Admins
•	10% Support Employees, at least 2 work groups
•	30% Regular Shift Employees, at least 2 work groups
•	53% Regular Day Employees, at least 2 work groups
•	5% Tolerance in the number of employees distribution across roles
"""


def role_groups(_num_groups) -> List[str]:
    """
    generate list of groups according to 'min_groups_for_roles' conditions.
    """
    _group_roles = []
    for role, min_groups in min_groups_for_roles.items():
        _group_roles += [role] * min_groups
    number_of_random_groups = _num_groups - len(_group_roles)
    _group_roles += np.random.choice(roles, number_of_random_groups).tolist()
    return _group_roles


group_roles = role_groups(num_groups)


# Function to randomly distribute users across groups while satisfying conditions
def size_groups(_total_users, _group_roles: List[str], _role_distribution, max_tolerance):
    while True:
        number_of_role_groups = {role: count for role, count in zip(*np.unique(_group_roles, return_counts=True))}
        _group_sizes = np.random.multinomial(
            _total_users,
            [_role_distribution[role] / number_of_role_groups[role] for role in _group_roles])
        # [_group_sizes[j] for j, role2 in enumerate(_group_roles) if role2 == role1]

        sum_of_role_users = {
            role1: sum([_group_sizes[j] for j, role2 in enumerate(_group_roles) if role2 == role1])
            for role1 in _role_distribution.keys()}
        if all([(sum_of_role_users[role] / _total_users - distribution) < max_tolerance
                for role, distribution in _role_distribution.items()]):
            return _group_sizes


# Randomly distribute users across groups
group_sizes = size_groups(total_employees, group_roles, role_distribution, role_distribution_tolerance)


def users_in_groups(_group_sizes, _group_roles):
    work_group_data = []
    user_id = 0
    for group_id in range(1, num_groups + 1):
        for _ in range(_group_sizes[group_id - 1]):
            work_group_data.append([user_id, group_id, _group_roles[group_id - 1]])
            user_id += 1
    return work_group_data


work_group_data = users_in_groups(group_sizes, group_roles)

work_group_df = pd.DataFrame(work_group_data, columns=['UserID', 'GroupID', 'Role'])


# Ensure the total count is still valid
def check_role_users_distribution(user_df, role_distribution):
    assert all([
        abs((len(user_df[user_df['Role'] == role]) / len(user_df)) - distribution) < role_distribution_tolerance
        for role, distribution in role_distribution.items()])


check_role_users_distribution()
