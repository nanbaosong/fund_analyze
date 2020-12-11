# -*- coding: utf-8 -*-d
from fund_info import *
import xlrd
import xlwt

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.      36'}
filename = 'all_fund_data.xls'

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
    return all_data


def wirte_to_file(data, file_path_name):
    excel = xlwt.Workbook()
    sheet = excel.add_sheet("0")
    row = 0
    for element in data:
        sheet.write(row, 0, element.base_info.name)
        sheet.write(row, 1, element.base_info.code)
        sheet.write(row, 2, element.base_info.fund_type)
        sheet.write(row, 3, element.base_info.risk_level)
        sheet.write(row, 4, element.base_info.fund_size)
        sheet.write(row, 5, element.base_info.current_manager)
        row = row + 1
    excel.save(file_path_name)

if __name__ == "__main__":
    root_url = 'http://fund.eastmoney.com/fundguzhi.html'
    all_data = get_all_data(root_url)
    selected_data = analyze(all_data)
    wirte_to_file(selected_data, filename)

