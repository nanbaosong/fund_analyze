# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from datetime import datetime

class BaseInfo(object):

    def __init__(self, info, name, code):
        self.name = name
        self.code = code
        all_data = info.find_all(name='td')
        if all_data:
            for td in all_data:
                key = td.text.split('：')[0]
                value = td.text.split('：')[1]
                if key == '基金类型':
                    self.fund_type = value.split('\xa0')[0]
                    self.risk_level = value.split('\xa0')[-1]
                if key == '基金规模':
                    self.fund_size = to_specific_value(value)
                    self.find_size_html = td.find(name='a')['href']
                if key == '基金经理':
                    self.current_manager = value
                    self.manager_html = td.find(name='a')['href']
                if key == '成 立 日':
                    self.create_date = value
                if key == '管 理 人':
                    self.organization = value
                    self.organization_html = td.find(name='a')['href']
                if key == '基金评级':
                    pic_string = td.find(name='div')['class'][0]
                    self.fund_rating_html = td.find(name='a')['href']
                    if len(pic_string) == 4:
                        self.fund_rating = 0
                    if len(pic_string) == 5:
                        self.fund_rating = int(pic_string[-1])

class ManagerInfo(object):

    def __init__(self, info):
        manager_peroid = info.find(name='div', attrs={'class': 'box'}).find(name='tbody').find_all(name='tr')
        self.manager_info_list = []
        if manager_peroid:
            for element in manager_peroid:
                self.manager_info_list.append(ManagerPeroidInfo(element))
        manager_names = info.find_all(name='div', attrs={'class': 'jl_intro'})
        self.manager_names_list = []
        self.manager_fund_info = []
        if manager_names:
            for manager_name in manager_names:
                name = manager_names.find(name='div', attrs={'class': 'text'}).find(name='p').find('a').text
                manager_names_list.append(name)
            manager_fund = info.find_all(name='div', attrs={'class': 'jl_office'})
            for element in manager_fund:
                infos = element.find(name='tbody').find_all(name='tr')
                tmp = []
                if infos:
                    for info in infos:
                        tmp.append(ManagerFundInfo(info))
                manager_fund_info.append(tmp)

class ManagerPeroidInfo:

    def __init__(self, info):
        all_data = info.find_all(name='td')
        for index,value in enumerate(all_data):
            if index == 0:
                self.start_date = value.text
            if index == 1:
                self.end_date = value.text
            if index == 2:
                self.manager_name = value.text
            if index == 3:
                self.period = value.text
            if index == 4:
                self.score = value.text

class ManagerFundInfo:

    def __init__(self, info):
        data = info.find_all(name='td')
        for index, value in enumerate(data):
            if index == 0:
                self.code = value.text
            if index == 1:
                self.name = value.text
            if index == 2:
                self.fund_type = value.text
            if index == 3:
                self.start_date = value.text
            if index == 4:
                self.end_date = value.text
            if index == 5:
                self.time = value.text
            if index == 6:
                self.increase_amount = value.text
            if index == 7:
                self.same_type_ave = value.text
            if index == 8:
                self.rank_rate = to_specific_value(value.text)

class IncreaseInfo(object):

    current_fund = {}
    same_type_ave = {}
    hushen_300 = {}
    rank = {}
    follow = {}
    level = {}

    def __init__(self, info):
        all_data = info.find_all(name='tr')
        for index,value in enumerate(all_data):
            if index != 0:
                self.get_data(value)
    
    def get_data(self, value):
        key = value.find(name='td')
        if key.text.strip() == '阶段涨幅':
            d = self.current_fund
        if key.text.strip() == '同类平均':
            d = self.same_type_ave
        if key.text.strip() == '沪深300':
            d = self.hushen_300
        if key.find(name='div', attrs={'class': 'infoTips'}) != None and key.contents[1].contents[0].strip() == '跟踪标的':
            d = self.follow
        if key.text.strip() == '同类排名':
            d = self.rank
        if key.find(name='div', attrs={'class': 'infoTips'}) != None and key.contents[1].contents[0].strip() == '四分位排名':
            d = self.level
        data = value.find_all(name='td')
        for sub_index, sub_value in enumerate(data):
            if sub_index == 1:
                d['oneWeek'] = to_specific_value(sub_value.text)
            if sub_index == 2:
                d['oneMonth'] = to_specific_value(sub_value.text)
            if sub_index == 3:
                d['threeMonth'] = to_specific_value(sub_value.text)
            if sub_index == 4:
                d['sixMonth'] = to_specific_value(sub_value.text)
            if sub_index == 5:
                d['currentYear'] = to_specific_value(sub_value.text)
            if sub_index == 6:
                d['oneYear'] = to_specific_value(sub_value.text)
            if sub_index == 7:
                d['twoYear'] = to_specific_value(sub_value.text)
            if sub_index == 8:
                d['threeYear'] = to_specific_value(sub_value.text)

def to_specific_value(st):
    st = st.strip()
    if st == '优秀' or st == '良好' or st == '一般' or st == '不佳':
        return st
    if st.find('--') != -1:
        return None
    if st.find('|') != -1:
        return float(st.split('|')[0]) / float(st.split('|')[-1])
    if st.find('%') != -1:
        st = st.split('%')[0]
    if st.find('亿') != -1:
        st = st.split('亿')[0]
    return float(st)