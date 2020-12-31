# -*- coding: utf-8 -*-d
from fund_data import *

all_manager_info = []

def analyze_manager(one_fund_info, manager_file):
    manager_name = get_good_manager(one_fund_info)
    if manager_name:
        manager_file.writelines(manager_name)
        manager_file.writelines('\n')
        manager_file.flush()

def analyze_one_fund(one_fund_info, fund_file, holding_file):
    if is_what_you_want(one_fund_info):
        fund_file.writelines(('%s  %s  %s  %s  %s  %s  %s') % (one_fund_info.base_info.code, one_fund_info.base_info.name, one_fund_info.base_info.fund_type,\
                        one_fund_info.base_info.create_date, one_fund_info.base_info.current_manager, one_fund_info.base_info.organization,\
                        one_fund_info.base_info.fund_size))
        if one_fund_info.holding_info:
            fund_file.writelines('  %s\n' % (one_fund_info.holding_info.internal))
        else:
            fund_file.writelines('  0.00%\n')
        fund_file.flush()
    
    if is_match_holding_filter(one_fund_info):
        holding_file.writelines(('%s  %s  %s  %s  %s  %s  %s  %s\n') % (one_fund_info.base_info.code, one_fund_info.base_info.name, one_fund_info.base_info.fund_type,\
                        one_fund_info.base_info.create_date, one_fund_info.base_info.current_manager, one_fund_info.base_info.organization,\
                        one_fund_info.base_info.fund_size, one_fund_info.holding_info.internal))
        holding_file.flush()


def is_match_holding_filter(input):
    fund_type = input.base_info.fund_type
    if fund_type == '债券型':
        if is_in_selected_size(input.base_info.fund_size, 5, 100) and is_in_selected_top_rank(input.increase_info, 0.50) and input.holding_info and input.holding_info.internal != '0.00%':
            return True
    else:
        if is_in_selected_size(input.base_info.fund_size, 10, 300) and is_better_than_hushen_300(input.increase_info) and is_in_selected_top_rank(input.increase_info, 0.30) and input.holding_info and input.holding_info.internal != '0.00%':
            return True
    return False    
    
    
def is_what_you_want(input):
    fund_type = input.base_info.fund_type
    if fund_type == '债券型':
        return is_what_you_want_bonds(input)
    return is_what_you_want_shares(input)

def is_what_you_want_bonds(input):
    if is_in_selected_size(input.base_info.fund_size, 5, 100):
        if is_in_selected_top_rank(input.increase_info, 0.20):
            if is_in_selected_top_rank_now(input.increase_info, 0.10):
                return True
    return False

def is_what_you_want_shares(input):
    if is_in_selected_size(input.base_info.fund_size, 10, 300):
        if is_better_than_hushen_300(input.increase_info):
            if is_in_selected_top_rank(input.increase_info, 0.20):
                if is_in_selected_top_rank_now(input.increase_info, 0.10):
                    return True
    return False

def get_good_manager(input):
    manager_name_list = input.manager_info.manager_name_list
    manager_fund_info_list = input.manager_info.manager_fund_info_list
    manager_career_length = input.manager_info.career_length
    for index, value in enumerate(manager_fund_info_list):
        if manager_name_list[index] in all_manager_info:
            return None
        all_manager_info.append(manager_name_list[index])
        for info in value:
            if manager_career_length[index] < 5 or\
               info.increase_amount and info.same_type_ave and info.increase_amount < info.same_type_ave or\
               info.rank_rate and info.rank_rate > 0.25:
               return None
        return manager_name_list[index]

def is_in_selected_top_rank(increase_info, rank_rate):
    rank = increase_info.rank
    if rank['oneWeek'] and rank['oneWeek'] < rank_rate and\
       rank['oneMonth'] and rank['oneMonth'] < rank_rate and\
       rank['threeMonth'] and rank['threeMonth'] < rank_rate and\
       rank['sixMonth'] and rank['sixMonth'] < rank_rate and\
       rank['currentYear'] and rank['currentYear'] < rank_rate and\
       rank['oneYear'] and rank['oneYear'] < rank_rate and\
       rank['twoYear'] and rank['twoYear'] < rank_rate and\
       rank['threeYear'] and rank['threeYear'] < rank_rate:
        return True
    return False

def is_in_selected_top_rank_now(increase_info, rank_rate):
    rank = increase_info.rank
    if rank['oneWeek'] and rank['oneWeek'] < rank_rate and\
       rank['oneMonth'] and rank['oneMonth'] < rank_rate and\
       rank['threeMonth'] and rank['threeMonth'] < rank_rate:
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
        current_fund['twoYear'] and current_fund['twoYear'] > hushen_300['twoYear'] and\
        current_fund['threeYear'] and current_fund['threeYear'] > hushen_300['threeYear']:
        return True
    return False


def is_in_selected_size(size, start, end):
    return size and size >= start and size <= end