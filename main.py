# -*- coding: utf-8 -*-d
from fund_info import *

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.      36'}

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
    all_fund_info = []
    for data in all_data:
        tmp = data.find(name='a')
        url = 'http://fund.eastmoney.com/' + tmp['href']
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

