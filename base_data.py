# -*- coding: utf-8 -*-
from utils import to_specific_value, trans_to_date, date_to_number

class BaseInfo(object):
    """
    基金基本信息
    """
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
                    self.create_date = trans_to_date(value)
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
    """
    基金经理信息
    """
    def __init__(self, info):
        self.manager_name_list = []
        self.manager_fund_info_list = []
        self.career_length = []
        self.manager_period_info_list = []
        if info:
            manager_peroid = info.find(name='div', attrs={'class': 'box'}).find(name='tbody').find_all(name='tr')
            if manager_peroid:
                for element in manager_peroid:
                    self.manager_period_info_list.append(ManagerPeroidInfo(element))
            manager_names = info.find_all(name='div', attrs={'class': 'jl_intro'})
            
            if manager_names:
                for manager_name in manager_names:
                    name = manager_name.contents[1].contents[0].contents[1].contents[0]
                    self.manager_name_list.append(name)
                manager_fund = info.find_all(name='div', attrs={'class': 'jl_office'})
                for element in manager_fund:
                    infos = element.find(name='tbody').find_all(name='tr')
                    tmp = []
                    if infos:
                        for info in infos:
                            tmp.append(ManagerFundInfo(info))
                    length = 2022 - int(tmp[-1].start_date.split('-')[0])
                    self.career_length.append(length)
                    self.manager_fund_info_list.append(tmp)

class ManagerPeroidInfo:
    """
    基金历任经理信息
    """
    def __init__(self, info):
        all_data = info.find_all(name='td')
        for index,value in enumerate(all_data):
            if index == 0:
                self.start_date = trans_to_date(value.text)
            if index == 1:
                self.end_date = trans_to_date(value.text)
            if index == 2:
                self.manager_name = value.text
            if index == 3:
                self.period = date_to_number(value.text)
            if index == 4:
                self.score = value.text

class ManagerFundInfo:
    """
    经理管理过的所有基金信息
    """
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
                self.start_date = trans_to_date(value.text)
            if index == 4:
                self.end_date = trans_to_date(value.text)
            if index == 5:
                self.time = date_to_number(value.text)
            if index == 6:
                self.increase_amount = to_specific_value(value.text)
            if index == 7:
                self.same_type_ave = to_specific_value(value.text)
            if index == 8:
                self.rank_rate = to_specific_value(value.text)

class IncreaseInfo(object):
    """
    基金阶段涨幅信息
    """
    def __init__(self, info):
        self.current_fund = {}
        self.same_type_ave = {}
        self.hushen_300 = {}
        self.rank = {}
        self.follow = {}
        self.level = {}
        all_data = info.find_all(name='tr')
        for index,value in enumerate(all_data):
            if index != 0:
                self.get_data(value)
    
    def get_data(self, value):
        key = value.find(name='td')
        if key.contents[1].contents[0].strip() == '阶段涨幅':
            d = self.current_fund
        elif key.contents[1].contents[0].strip() == '同类平均':
            d = self.same_type_ave
        elif key.contents[1].contents[0].strip() == '沪深300':
            d = self.hushen_300
        elif key.contents[1].contents[0].strip() == '跟踪标的':
            d = self.follow
        elif key.contents[1].contents[0].strip() == '同类排名':
            d = self.rank
        elif key.contents[1].contents[0].strip() == '四分位排名':
            d = self.level
        else:
            return
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

class PositionInfo(object):
    """
    基金持仓信息
    """
    def __init__(self, info):
        self.position_list = []
        if info:
            info_list = info.find_all(name='tr')
            if len(info_list) > 1:
                for index, value in enumerate(info_list):
                    if index != 0:
                        real_value_list = value.find_all(name='td')
                        if len(real_value_list) >= 2:
                            position_name = real_value_list[0].text.strip()
                            position_url = None
                            if real_value_list[0].find(name='a'):
                                position_url = real_value_list[0].find(name='a')['href']
                            position_rate = real_value_list[1].text
                            self.position_list.append(ShareBondsPostionInfo(position_name, position_url, position_rate))

class ShareBondsPostionInfo(object):
    """
    持仓股票/债券 信息
    """
    def __init__(self, name, url, rate):
        self.name = name
        self.url = url
        self.rate = to_specific_value(rate)

class HoldingInfo(object):
    """
    持有人 信息
    """

    def __init__(self, info):
        self.date = trans_to_date('')
        self.group = '0.00%'
        self.person = '0.00%'
        self.internal = '0.00%'
        self.all_number = '0.0'
        if info:
            data = info.find_all(name='td')
            for index, value in enumerate(data):
                if index == 0:
                    self.date = trans_to_date(value.text)
                if index == 1:
                    self.group = value.text
                if index == 2:
                    self.person = value.text
                if index == 3:
                    self.internal = value.text
                if index == 4:
                    self.all_number = value.text

class SpecialInfo(object):
    """
    基金特色数据
    """

    def __init__(self, info):
        self.sp = {}
        self.sd = {}
        if info:
            data = info.find_all(name='tr')
            for index, value in enumerate(data):
                if index == 1:
                    d = value.find_all(name='td')
                    for k, v in enumerate(d):
                        if k == 1:
                            self.sd['oneYear'] = to_specific_value(v.text)
                        if k == 2:
                            self.sd['twoYear'] = to_specific_value(v.text)
                        if k == 3:
                            self.sd['threeYear'] = to_specific_value(v.text)
                if index == 2:
                    d = value.find_all(name='td')
                    for k, v in enumerate(d):
                        if k == 1:
                            self.sp['oneYear'] = to_specific_value(v.text)
                        if k == 2:
                            self.sp['twoYear'] = to_specific_value(v.text)
                        if k == 3:
                            self.sp['threeYear'] = to_specific_value(v.text)

    