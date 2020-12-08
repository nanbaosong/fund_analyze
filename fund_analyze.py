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

    def set_base_info(self, info, name, code):
        self.base_info = BaseInfo(info, name, code)

    def set_manager_info(self, info):
        self.manager_info = ManagerInfo(self.base_info.manager_html)

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
