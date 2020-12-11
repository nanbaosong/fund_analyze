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
                    self.fund_size = to_float(value)
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

class Increase(object):
    current_fund = {}
    same_type_ave = {}
    hushen_300 = {}
    rank = {}
    def __init__(self, info):
        all_data = info.find_all(name='tr')
        for index,value in enumerate(all_data):
            # need to do next time
            if index != 0 and index < 5:
                self.get_data(value, index)
    
    def get_data(self, value, index):
        data = value.find_all(name='td')
        if index == 1:
            d = self.current_fund
        if index == 2:
            d = self.same_type_ave
        if index == 3:
            d = self.hushen_300
        if index == 4:
            d = self.rank
        for sub_index, sub_value in enumerate(data):
            if sub_index == 1:
                d['oneWeek'] = to_float(sub_value.text)
            if sub_index == 2:
                d['oneMonth'] = to_float(sub_value.text)
            if sub_index == 3:
                d['threeMonth'] = to_float(sub_value.text)
            if sub_index == 4:
                d['sixMonth'] = to_float(sub_value.text)
            if sub_index == 5:
                d['currentYear'] = to_float(sub_value.text)
            if sub_index == 6:
                d['oneYear'] = to_float(sub_value.text)
            if sub_index == 7:
                d['twoYear'] = to_float(sub_value.text)
            if sub_index == 8:
                d['threeYear'] = to_float(sub_value.text)

def to_float(st):
    if st.find('--') != -1:
        return -100000.0
    if st.find('|') != -1:
        return float(st.split('|')[0]) / float(st.split('|')[-1])
    if st.find('%') != -1:
        st = st.split('%')[0]
    if st.find('亿') != -1:
        st = st.split('亿')[0]
    return float(st)