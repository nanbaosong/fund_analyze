# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from datetime import datetime

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.      36'}

class PriceInfo(object):
    pass

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


class ManagerInfo(object):
    manager_info_list = []

    def __init__(self, info):
        manager_peroid = info.find(name='div', attrs={'class': 'box'}).find(name='tbody').find_all(name='tr')
        if manager_peroid:
            for element in manager_peroid:
                self.manager_info_list.append(ManagerPeroidInfo(element))
 
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
                    self.fund_size = float(value.split('亿')[0])
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


class FundInfo(object):

    def __init__(self, all_info, name, code):
        base_info = all_info.find(name='div', attrs={'class': 'infoOfFund'})
        self.set_base_info(base_info, name, code)
        self.set_manager_info()
        pass

    def set_base_info(self, info, name, code):
        self.base_info = BaseInfo(info, name, code)

    def set_manager_info(self):
        manager_info_html = requests.get(self.base_info.manager_html)
        manager_info_html.encoding='utf-8'
        soup = BeautifulSoup(manager_info_html.text, 'lxml')
        self.manager_info = ManagerInfo(soup)

    def set_prices_info(self, info):
        self.price_info = PriceInfo(info)

def get_one_fund_info(url, name, code):
    html = requests.get(url, headers)
    html.encoding='utf-8'
    soup = BeautifulSoup(html.text, 'lxml')
    fund_info = FundInfo(soup, name, code)
    return fund_info

def get_all_data(root_url):
    root_html = requests.get(root_url, headers)
    root_html.encoding='gb2312'
    root_soup = BeautifulSoup(root_html.text, 'lxml')
    all_data = root_soup.find(name='tbody', attrs={'id': 'tableContent'}).find_all(name='td', attrs={'class': 'ui-table-left'})
    url = 'http://fund.eastmoney.com/'
    all_fund_info = []
    for data in all_data:
        tmp = data.find(name='a')
        url = url + tmp['href']
        name = tmp.text
        one_fund_info = get_one_fund_info(url, name, tmp['href'].split('.')[0])
        all_fund_info.append(one_fund_info)
    return all_fund_info

def analyze(all_data):
    pass


if __name__ == "__main__":
    root_url = 'http://fund.eastmoney.com/fundguzhi.html'
    all_data = get_all_data(root_url)
    analyze(all_data)

