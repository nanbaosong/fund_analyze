# -*- coding: utf-8 -*-d
from fund_data import *

def is_what_you_want(input):
    if is_in_selected_size(input.base_info.fund_size, 10, 350):
        if is_in_selected_top_rank(input.increase_info, 0.25):
            if is_better_than_hushen_300(input.increase_info):
                return True
    return False

def is_in_selected_top_rank(increase_info, rank_rate):
    rank = increase_info.rank
    if rank['oneWeek'] < rank_rate and rank['oneWeek'] != -100000.0 and\
       rank['oneMonth'] < rank_rate and rank['oneMonth'] != -100000.0 and\
       rank['threeMonth'] < rank_rate and rank['threeMonth'] != -100000.0 and\
       rank['sixMonth'] < rank_rate and rank['sixMonth'] != -100000.0 and\
       rank['currentYear'] < rank_rate and rank['currentYear'] != -100000.0 and\
       rank['oneYear'] < rank_rate and rank['oneYear'] != -100000.0 and\
       rank['twoYear'] < rank_rate and rank['twoYear'] != -100000.0:
        return True
    return False

def is_better_than_hushen_300(increase_info):
    hushen_300 = increase_info.hushen_300
    current_fund = increase_info.current_fund
    if  current_fund['oneWeek'] > hushen_300['oneWeek'] and \
        current_fund['oneMonth'] > hushen_300['oneMonth'] and\
        current_fund['threeMonth'] > hushen_300['threeMonth'] and\
        current_fund['sixMonth'] > hushen_300['sixMonth'] and\
        current_fund['currentYear'] > hushen_300['currentYear'] and\
        current_fund['oneYear'] > hushen_300['oneYear'] and\
        current_fund['twoYear'] > hushen_300['twoYear']:
        return True
    return False


def is_in_selected_size(size, start, end):
    return size >= start and size <= end