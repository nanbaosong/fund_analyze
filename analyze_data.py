# -*- coding: utf-8 -*-d
from fund_data import *

all_manager_info = []


def is_what_you_want_fund(input):
    fund_type = input.base_info.fund_type
    if fund_type == '债券型':
        return is_what_you_want_bonds(input)
    return is_what_you_want_shares(input)

def is_what_you_want_bonds(input):
    if is_in_selected_size(input.base_info.fund_size, 3, 100):
        if is_in_selected_top_rank(input.increase_info, 0, 6, 0.25):
            if is_in_selected_top_rank(input.increase_info,0, 3, 0.10):
                return True
    return False

def is_what_you_want_shares(input):
    if is_in_selected_size(input.base_info.fund_size, 5, 300):
        if is_better_than_hushen_300(input.increase_info, 2, 6):
            if is_in_selected_top_rank(input.increase_info, 3, 6, 0.30):
                    return True
    return False

def get_what_you_want_manager(manager_info):
    manager_name_list = manager_info.manager_name_list
    manager_fund_info_list = manager_info.manager_fund_info_list
    manager_career_length = manager_info.career_length
    name_list = []
    fund_info_list = []
    for index, value in enumerate(manager_fund_info_list):
        flag = False
        for info in value:
            if len(value) > 10 or\
               manager_career_length[index] < 6 or\
               info.increase_amount and info.same_type_ave and info.increase_amount < info.same_type_ave or\
               info.rank_rate and info.rank_rate > 0.30:
               flag = True
               break
        if not flag:
            name_list.append(manager_name_list[index])
            fund_info_list.append(value)
    return name_list, fund_info_list

def is_in_selected_top_rank(increase_info, start, end, rank_rate):
    time = ['oneWeek', 'oneMonth', 'threeMonth', 'sixMonth', 'oneYear', 'twoYear', 'threeYear']
    rank = increase_info.rank
    for index in range(start, end + 1):
        if not rank[time[index]] or rank[time[index]] > rank_rate:
            return False
    return True

def is_better_than_hushen_300(increase_info, start, end):
    hushen_300 = increase_info.hushen_300
    time = ['oneWeek', 'oneMonth', 'threeMonth', 'sixMonth', 'oneYear', 'twoYear', 'threeYear']
    current_fund = increase_info.current_fund
    for index in range(start, end + 1):
        if not current_fund[time[index]] or current_fund[time[index]] < hushen_300[time[index]]:
            return False
    return True


def is_in_selected_size(size, start, end):
    return size and size >= start and size <= end