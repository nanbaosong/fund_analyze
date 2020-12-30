# -*- coding: utf-8 -*-d
from fund_data import *
from analyze_data import *

filename = 'whatYouWant.txt'
manager_filename = 'good_manager.txt'
holding_filename = 'holding.txt'

def get_one_fund_info(url, name, code):
    html = requests.get(url, headers)
    html.encoding='utf-8'
    soup = BeautifulSoup(html.text, "html.parser")
    #如果网页重定向就更新url
    redirect = soup.find(name='head').find(name='script', attrs={'type': 'text/javascript'})
    if redirect != None and redirect.contents[0] != None:
        real_url = redirect.contents[0].split('"')[1]
        html = requests.get(real_url, headers)
        html.encoding='utf-8'
        soup = BeautifulSoup(html.text, 'lxml')
    fund_info = FundInfo(soup, name, code)
    return fund_info

def get_all_data(root_url):
    # 获取所有基金的code和name 
    root_html = requests.get(root_url, headers)
    root_html.encoding='utf-8'
    tmp_str = root_html.text.split('=')[-1].split(';')[0]
    all_data = eval(tmp_str)
    all_fund_info = []
    fund_file = open(filename, 'w')
    manager_file = open(manager_filename, 'w')
    holding_file = open(holding_filename, 'w')
    # 逐个爬取数据
    for data in all_data:
        url = 'http://fund.eastmoney.com/' + data[0] + '.html'
        print('==== start to get data of %s %s ===='%(data[0], data[2]))
        one_fund_info = get_one_fund_info(url, data[2], data[0])
        print('==== end to get data of %s %s ===='%(data[0], data[2]))
        # all_fund_info.append(one_fund_info)
        # 根据条件筛选基金
        analyze_one_fund(one_fund_info, fund_file, holding_file)
        # 根据条件筛选基金经理
        analyze_manager(one_fund_info, manager_file)
    fund_file.close()
    manager_file.close()
    holding_file.close()
    return all_fund_info

if __name__ == "__main__":
    root_url = 'http://fund.eastmoney.com/js/fundcode_search.js'
    all_data = get_all_data(root_url)
