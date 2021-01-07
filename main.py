# -*- coding: utf-8 -*-d
from fund_data import *
from analyze_data import *
from write_data import *

es_list = [{'host':'127.0.0.1','port':9200}]
fund_info_index = 'fund_info'
manager_info_index = 'manager_info'
selected_fund_info_index = 'selected_fund_info'
selected_manager_info_index = 'selected_manager_info'

all_index = [fund_info_index, manager_info_index, selected_fund_info_index, selected_manager_info_index]

all_selected_manager_name_info = []
all_manager_name_info = []


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
    es = Elasticsearch(es_list)
    # 删除es下index的数据，避免重复写入
    for index in all_index:
        if delete_index_es(es, index) == False:
            print('terminal program')
            return

    # 获取所有基金的code和name 
    root_html = requests.get(root_url, headers)
    root_html.encoding='utf-8'
    tmp_str = root_html.text.split('=')[-1].split(';')[0]
    all_data = eval(tmp_str)

    # 逐个爬取数据
    for data in all_data:
        url = 'http://fund.eastmoney.com/' + data[0] + '.html'
        print('==== start to get data of %s %s ===='%(data[0], data[2]))
        one_fund_info = get_one_fund_info(url, data[2], data[0])
        print('==== end to get data of %s %s ===='%(data[0], data[2]))
        
        # 将基金信息写入es
        write_fund_info_to_es(one_fund_info, es, fund_info_index)
        # 将基金经理信息写入es
        manager_info = one_fund_info.manager_info
        manager_name_list, manager_fund_info_list = remove_duplicate(manager_info.manager_name_list, manager_info.manager_fund_info_list, all_manager_name_info)
        write_manager_info_to_es(manager_name_list, manager_fund_info_list, es, manager_info_index)

        # 根据条件筛选基金
        if is_what_you_want_fund(one_fund_info):
            write_fund_info_to_es(one_fund_info, es, selected_fund_info_index)
        # 根据条件筛选基金经理
        manager_name_list, manager_fund_info_list = get_what_you_want_manager(manager_info)
        selected_manager_name_list, selected_manager_fund_info_list = remove_duplicate(manager_name_list, manager_fund_info_list, all_selected_manager_name_info)
        write_manager_info_to_es(selected_manager_name_list, selected_manager_fund_info_list, es, selected_manager_info_index)

if __name__ == "__main__":
    root_url = 'http://fund.eastmoney.com/js/fundcode_search.js'
    get_all_data(root_url)
