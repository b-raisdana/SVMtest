from typing import List

import numpy as np
import pandas as pd

import config

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
    for role, min_groups in config.min_groups_for_roles.items():
        _group_roles += [role] * min_groups
    number_of_random_groups = _num_groups - len(_group_roles)
    _group_roles += np.random.choice(config.roles, number_of_random_groups).tolist()
    return _group_roles


group_roles = role_groups(config.num_groups)


def is_sized_work_group(summary):
    if (abs(summary['Population'].sum() - config.total_employees) / config.total_employees >
            config.role_distribution_tolerance):
        return False
    summary['Proportion'] = summary['Population'] / summary['Population'].sum()
    summary['Expected Proportion'] = [config.role_distribution[role] for role in summary['Role']]
    summary['Proportion Deviation'] = abs(summary['Proportion'] - summary['Expected Proportion'])
    return all(summary['Proportion Deviation'] <= config.role_distribution_tolerance)


# Function to randomly distribute users across groups while satisfying conditions
def size_groups(_total_users, _group_roles: List[str], _role_distribution, max_tolerance):
    while True:
        # {'Admin': 1, 'Regular Day': 3, 'Regular Shift': 3, 'Support Day': 1, 'Support Shift': 2}
        number_of_role_groups = {role: count for role, count in zip(*np.unique(_group_roles, return_counts=True))}
        _group_sizes = np.random.multinomial(
            _total_users,
            [_role_distribution[role] / number_of_role_groups[role] for role in _group_roles])
        _groups_df = pd.DataFrame(list(zip(_group_roles, _group_sizes)), columns=['Role', 'Size'])
        _groups_summary = _groups_df.groupby('Role').agg('sum').reset_index().rename(columns={'Size': 'Population'})
        # # _groups_summary['Proportion'] = _groups_summary['Size'] / _groups_summary['Size'].sum()
        # # _groups_summary['Expected Proportion'] = [config.role_distribution[role] for role in _groups_summary.index]
        # # pd.DataFrame([(role, _role_distribution[role] / number_of_role_groups[role]) for role in _group_roles],
        # #              columns=['Role', 'Propotion']).groupby(
        # #     'Role').agg('sum')
        # # # [_group_sizes[j] for j, role2 in enumerate(_group_roles) if role2 == role1]
        # #
        # # sum_of_role_users = {
        # #     role1: sum([_group_sizes[j] for j, role2 in enumerate(_group_roles) if role2 == role1])
        # #     for role1 in _role_distribution.keys()}
        # if all([(sum_of_role_users[role] / _total_users - distribution) < max_tolerance
        #         for role, distribution in _role_distribution.items()]):
        if is_sized_work_group(_groups_summary):
            return _group_sizes


# Randomly distribute users across groups
group_sizes = size_groups(config.total_employees, group_roles, config.role_distribution,
                                                     config.role_distribution_tolerance)


def users_in_groups(_group_sizes, _group_roles):
    _work_group_data = []
    user_id = 0
    for group_id in range(1, config.num_groups + 1):
        for _ in range(_group_sizes[group_id - 1]):
            _work_group_data.append([user_id, group_id, _group_roles[group_id - 1]])
            user_id += 1
    return _work_group_data


work_group_data = users_in_groups(group_sizes, group_roles)

workgroup = pd.DataFrame(work_group_data, columns=['UserID', 'GroupID', 'Role'])


def verify_work_group(_workgroup):
    summary = _workgroup.groupby(['Role']).size().reset_index().rename(columns={0: 'Population'})
    assert is_sized_work_group(summary)


verify_work_group(workgroup)

workgroup.to_csv("../Data/workgroups.csv", index=False)

# # Ensure the total count is still valid
# def check_role_users_distribution(_workgroup, _role_distribution):
#     _group_sizes = _workgroup.groupby('GroupID').agg('count')
#     _group_sizes = _workgroup.groupby(['GroupID', 'Role']).size().reset_index()
#     assert all([
#         abs((len(_workgroup[_workgroup['Role'] == role]) / len(
#             _workgroup)) - distribution) <= config.role_distribution_tolerance
#         for role, distribution in _role_distribution.items()])
#
#
# check_role_users_distribution(workgroup, config.role_distribution)
