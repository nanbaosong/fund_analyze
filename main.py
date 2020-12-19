# -*- coding: utf-8 -*-d
from fund_data import *
from analyze_data import *

filename = 'whatYouWant.txt'
manager_filename = 'good_manager.txt'

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
    file = open(filename, 'w')
    manager_file = open(manager_filename, 'w')
    # 逐个爬取数据
    for data in all_data:
        url = 'http://fund.eastmoney.com/' + data[0] + '.html'
        print('==== start to get data of %s %s ===='%(data[0], data[2]))
        one_fund_info = get_one_fund_info(url, data[2], data[0])
        print('==== end to get data of %s %s ===='%(data[0], data[2]))
        all_fund_info.append(one_fund_info)
        # 根据条件筛选基金
        if is_what_you_want(one_fund_info):
            file.writelines(('%s  %s  %s  %s  %s  %s  %s  %s\n') % (one_fund_info.base_info.code, one_fund_info.base_info.name, one_fund_info.base_info.fund_type,\
                            one_fund_info.base_info.create_date, one_fund_info.base_info.current_manager, one_fund_info.base_info.organization,\
                            one_fund_info.base_info.fund_size, one_fund_info.base_info.fund_rating))
            file.flush()
        # 根据条件筛选基金经理
        manager_name = get_good_manager(one_fund_info)
        if manager_name:
            manager_file.writelines(manager_name)
            manager_file.writelines('\n')
            manager_file.flush()
    file.close()
    manager_file.close()
    return all_fund_info

if __name__ == "__main__":
    root_url = 'http://fund.eastmoney.com/js/fundcode_search.js'
    all_data = get_all_data(root_url)
