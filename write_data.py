# -*- coding: utf-8 -*-d
from fund_data import *
from elasticsearch import Elasticsearch

def write_fund_info_to_es(one_fund_info, es, fund_info_index):
    """
    将基金数据写入es
    """
    if one_fund_info.base_info.create_date == '--' and one_fund_info.base_info.fund_size == None:
        return
    dic_value = get_fund_info_dic_value(one_fund_info)
    write_to_es(es, dic_value, fund_info_index)
    

def get_fund_info_dic_value(one_fund_info):
    """
    将FundInfo类实例转成dictionary形式
    """
    data = {}
    if one_fund_info.base_info:
        data['baseInfo'] = simple_class_to_dict(one_fund_info.base_info)
    if one_fund_info.increase_info:
        data['increaseInfo'] = simple_class_to_dict(one_fund_info.increase_info)
    if one_fund_info.special_info:
        data['specialInfo'] = simple_class_to_dict(one_fund_info.special_info)
    if one_fund_info.holding_info:
        data['holdingInfo'] = simple_class_to_dict(one_fund_info.holding_info)
    if one_fund_info.manager_info:
        tmp = []
        for value in one_fund_info.manager_info.manager_period_info_list:
            tmp.append(simple_class_to_dict(value))
        data['managerPeriodInfo'] = tmp
    if one_fund_info.shares_info:
        tmp = []
        for value in one_fund_info.shares_info.position_list:
            tmp.append(simple_class_to_dict(value))
        data['shareInfo'] = tmp
    if one_fund_info.bonds_info:
        tmp = []
        for value in one_fund_info.bonds_info.position_list:
            tmp.append(simple_class_to_dict(value))
        data['bondsInfo'] = tmp
    return data

def write_manager_info_to_es(manager_name_list, manager_fund_info_list, es, manager_info_index):
    """
    将基金经理数据写入es
    """
    data = {}
    for index, value in enumerate(manager_fund_info_list):
        data['managerName'] = manager_name_list[index]
        tmp = []
        for info in value:
            tmp.append(simple_class_to_dict(info))
        data['managerCareer'] = tmp
        write_to_es(es, data, manager_info_index)

    
def simple_class_to_dict(obj):
    """
    将简单类（只有基本类型的成员变量的类）实例转成dictionary形式
    """
    pr = {}
    for name in dir(obj):
        value = getattr(obj, name)
        if not name.startswith('__') and not callable(value) and not name.startswith('_'):
            pr[name] = value
    return pr


def write_to_es(es, value, index):
    """
    将数据写入es
    """
    write_result = es.index(index, body=value, doc_type='doc')
    if write_result == False:
        print(('write data to es %s index failed') % (index))
    else:
        print(('write data to es %s index succeed') % (index))

def delete_index_es(es, index):
    delete_result = es.indices.delete(index=index, ignore=[400, 404])
    if delete_result == False:
        print(('fail to delete index %s in es') % (index))
    else:
        print(('delete index %s in es success') % (index))
    return delete_result

def remove_duplicate(manager_name_list, manager_fund_info_list, all_manager_name_info):
    name_list = []
    fund_info_list = []
    for index, value in enumerate(manager_name_list):
        if manager_name_list[index] not in all_manager_name_info:
            name_list.append(value)
            fund_info_list.append(manager_fund_info_list[index])
            all_manager_name_info.append(value)
    return name_list, fund_info_list
