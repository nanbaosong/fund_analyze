# -*- coding: utf-8 -*-d
from fund_data import *

all_manager_info = []

def is_what_you_want(input):
    if is_in_selected_size(input.base_info.fund_size, 10, 350):
        if is_in_selected_top_rank(input.increase_info, 0.25):
            if is_better_than_hushen_300(input.increase_info):
                return True
    return False

def get_good_manager(input):
    manager_names_list = input.manager_info.manager_names_list
    manager_fund_info = input.manager_info.manager_fund_info
    for index, value in enumerate(manager_fund_info):
        if manager_names_list[index] in all_manager_info:
            return None
        all_manager_info.append(manager_names_list[index])
        for info in value:
            if info.increase_amount and info.same_type_ave and info.increase_amount < info.same_type_ave or\
               info.rank_rate and info.rank_rate > 0.25:
               return None
        return manager_names_list[index]

def is_in_selected_top_rank(increase_info, rank_rate):
    rank = increase_info.rank
    if rank['oneWeek'] and rank['oneWeek'] < rank_rate and\
       rank['oneMonth'] and rank['oneMonth'] < rank_rate and\
       rank['threeMonth'] and rank['threeMonth'] < rank_rate and\
       rank['sixMonth'] and rank['sixMonth'] < rank_rate and\
       rank['currentYear'] and rank['currentYear'] < rank_rate and\
       rank['oneYear'] and rank['oneYear'] < rank_rate and\
       rank['twoYear'] and rank['twoYear'] < rank_rate:
        return True
    return False

def is_better_than_hushen_300(increase_info):
    hushen_300 = increase_info.hushen_300
    current_fund = increase_info.current_fund
    if  current_fund['oneWeek'] and current_fund['oneWeek'] > hushen_300['oneWeek'] and \
        current_fund['oneMonth'] and current_fund['oneMonth'] > hushen_300['oneMonth'] and\
        current_fund['threeMonth'] and current_fund['threeMonth'] > hushen_300['threeMonth'] and\
        current_fund['sixMonth'] and current_fund['sixMonth'] > hushen_300['sixMonth'] and\
        current_fund['currentYear'] and current_fund['currentYear'] > hushen_300['currentYear'] and\
        current_fund['oneYear'] and current_fund['oneYear'] > hushen_300['oneYear'] and\
        current_fund['twoYear'] and current_fund['twoYear'] > hushen_300['twoYear']:
        return True
    return False


def is_in_selected_size(size, start, end):
    return size and size >= start and size <= end