# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from datetime import datetime

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.      36'}

class ManagerInfo(object):
    pass
 
class PriceInfo(object):
    pass
 
class BaseInfo(object):

    def __init__(self, info, name, code):
        self.name = name
        self.code = code
        all_data = info.find_all(name='td')
        for data in all_data:
            


class FundInfo(object):

    def __init__(self, all_info, name, code):
        base_info = all_info.find(name='div', attrs={'class': 'infoOfFund'})
        fund_info.set_base_info(base_info, name, code)

    def set_base_info(self, info, name, code):
        self.base_info = BaseInfo(info, name, code)
    def set_manager_info(self, info):
        self.manager_info = ManagerInfo(info)
    def set_prices_info(self, info):
        self.price_info = PriceInfo(info)

def get_one_fund_info(url, name, code):
    html = requests.get(url, headers)
    html.encoding='utf-8'
    soup = BeautifulSoup(html.text, 'lxml')
    fund_info = FundInfo(soup, name, code)

def get_all_data(root_url):
    root_html = requests.get(root_url, headers)
    root_html.encoding='gb2312'
    root_soup = BeautifulSoup(root_html.text, 'lxml')
    all_data = root_soup.find(name='tbody', attrs={'id': 'tableContent'}).find_all(name='td', attrs={'class': 'ui-table-left'})
    url = 'http://fund.eastmoney.com/'
    for data in all_data:
        tmp = data.find(name='a')
        url = url + tmp['href']
        name = tmp.text
        get_one_fund_info(url, name, tmp['href'].split('.')[0])

if __name__ == "__main__":
    root_url = 'http://fund.eastmoney.com/fundguzhi.html'
    get_all_data(root_url)
