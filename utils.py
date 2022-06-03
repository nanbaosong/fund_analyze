import requests
import time
from requests.adapters import HTTPAdapter

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 Edg/101.0.1210.53'}


def to_specific_value(st):
    st = st.strip()
    if st.find('--') != -1 or (st.find('-') != -1 and st.find('|') != -1) or st == '':
        return None
    if st == '优秀' or st == '良好' or st == '一般' or st == '不佳':
        return st
    if st.find('|') != -1:
        return float(st.split('|')[0]) / float(st.split('|')[-1])
    if st.find('%') != -1:
        st = st.split('%')[0]
    if st.find('亿') != -1:
        st = st.split('亿')[0]
    return float(st)

def date_to_number(date):
    if date == '':
        return 0.0
    if date.find('年') == -1:
        day = date.split('天')[0]
        return float(day) / 365.0
    year = date.split('年')[0]
    if date.find('天') == -1:
        return float(year)
    else:
        day = date.split('又')[-1].split('天')[0]
        return float(year) + float(day) / 365.0

def trans_to_date(text):
    text = text.strip()
    if text == '至今' or text == '':
        return time.strftime("%Y-%m-%d",time.localtime(time.time()))
    return text

def get_html_from_url(url):
    html = None
    s = requests.Session()
    s.mount('http://', HTTPAdapter(max_retries=3))
    try:
        html = s.get(url, headers=header, timeout=10)
    except Exception as e:
        print(e)
    finally:
        return html

def remove_duplicate(manager_name_list, manager_fund_info_list, all_manager_name_info):
    name_list = []
    fund_info_list = []
    for index, value in enumerate(manager_name_list):
        if manager_name_list[index] not in all_manager_name_info:
            name_list.append(value)
            fund_info_list.append(manager_fund_info_list[index])
            all_manager_name_info.append(value)
    return name_list, fund_info_list
    

def remove_same_fund(all_data):
    for data in all_data:
        name = data[2]
        if name[-1] == 'C' or name[-4:] == "(后端)":
            all_data.remove(data)