# -*- coding: utf-8 -*-d
from fund_data import *
import xlrd
import xlwt

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.      36'}
filename = 'all_fund_data.xls'

def get_one_fund_info(url, name, code):
    html = requests.get(url, headers)
    html.encoding='utf-8'
    soup = BeautifulSoup(html.text, "html.parser")
    redirect = soup.find(name='head').find(name='script', attrs={'type': 'text/javascript'})
    if redirect != None and redirect.contents[0] != None:
        real_url = redirect.contents[0].split('"')[1]
        html = requests.get(real_url, headers)
        html.encoding='utf-8'
        soup = BeautifulSoup(html.text, 'lxml')
    fund_info = FundInfo(soup, name, code)
    return fund_info

def get_all_data(root_url):
    root_html = requests.get(root_url, headers)
    root_html.encoding='utf-8'
    tmp_str = root_html.text.split('=')[-1].split(';')[0]
    all_data = eval(tmp_str)
    all_fund_info = []
    file = open('whatYouWant.txt', 'w')
    for data in all_data:
        url = 'http://fund.eastmoney.com/' + data[0] + '.html'
        print('==== start to get data of %s %s ===='%(data[0], data[2]))
        one_fund_info = get_one_fund_info(url, data[2], data[0])
        print('==== end to get data of %s %s ===='%(data[0], data[2]))
        get_what_you_want(one_fund_info, file)
        all_fund_info.append(one_fund_info)
    file.close()
    return all_fund_info

def get_what_you_want(input, file):
    same_type_ave = input.increase_info.same_type_ave
    if input.base_info.fund_size > 30 and same_type_ave['oneWeek'] < 0.3 and same_type_ave['oneMonth'] < 0.3 and same_type_ave['threeMonth'] < 0.3 and same_type_ave['sixMonth'] < 0.3 and same_type_ave['currentYear'] < 0.3 and same_type_ave['oneYear'] < 0.3 and same_type_ave['twoYear'] < 0.3:
        file.writelines(input.base_info.code)
        file.write('\n')

        
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
    root_url = 'http://fund.eastmoney.com/js/fundcode_search.js'
    all_data = get_all_data(root_url)
    selected_data = analyze(all_data)
    wirte_to_file(selected_data, filename)

