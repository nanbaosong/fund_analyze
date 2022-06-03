# -*- coding: utf-8 -*-d
from fund_data import FundInfo
from bs4 import BeautifulSoup
from utils import get_html_from_url, remove_duplicate
from write_data import write_fund_info_to_es, write_manager_info_to_es, delete_index_es
import threading
import numpy
from elasticsearch import Elasticsearch

es_list = [{'host':'127.0.0.1','port':9200}]
fund_info_index = 'fund_info'
manager_info_index = 'manager_info'
thread_num = 4
all_index = [fund_info_index, manager_info_index]
all_manager_name_info = []


def get_one_fund_info(url, name, code):
    fund_info = None
    html = get_html_from_url(url)
    if html:
        html.encoding='utf-8'
        soup = BeautifulSoup(html.text, "html.parser")
        # 如果网页重定向就更新url
        redirect = soup.find(name='head').find(name='script', attrs={'type': 'text/javascript'})
        if redirect != None and redirect.contents[0] != None and 'location.href' in redirect.contents[0]:
            real_url = redirect.contents[0].split('"')[1]
            html = get_html_from_url(real_url)
            if html:
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
    root_html = get_html_from_url(root_url)
    if root_html:
        root_html.encoding='utf-8'
        tmp_str = root_html.text.split('=')[-1].split(';')[0]
        all_data = eval(tmp_str)
        threads = []
        data = numpy.array_split(all_data, thread_num)
        for value in data:
            t = threading.Thread(target=work_func, args=(value, es))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

def work_func(all_data, es):
    # 逐个爬取数据
        for data in all_data:
            url = 'http://fund.eastmoney.com/' + data[0] + '.html'
            print('==== start to get data of %s %s ===='%(data[0], data[2]))
            one_fund_info = get_one_fund_info(url, data[2], data[0])
            print('==== end to get data of %s %s ===='%(data[0], data[2]))

            if one_fund_info:
                # 将基金信息写入es
                write_fund_info_to_es(one_fund_info, es, fund_info_index)
                # 将基金经理信息写入es
                manager_info = one_fund_info.manager_info
                manager_name_list, manager_fund_info_list = remove_duplicate(manager_info.manager_name_list, manager_info.manager_fund_info_list, all_manager_name_info)
                write_manager_info_to_es(manager_name_list, manager_fund_info_list, es, manager_info_index)

if __name__ == "__main__":
    root_url = 'http://fund.eastmoney.com/js/fundcode_search.js'
    get_all_data(root_url)
