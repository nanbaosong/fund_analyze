from base_data import * 
import time

class FundInfo(object):

    def __init__(self, all_info, name, code):
        self.set_base_info(all_info, name, code)
        self.set_manager_info()
        self.set_increase_info(all_info)
        self.set_shares_info(all_info)
        self.set_bonds_info(all_info)
        # self.set_industry_info(code)

    # 获取基金基本信息
    def set_base_info(self, all_info, name, code):
        info = all_info.find(name='div', attrs={'class': 'infoOfFund'})
        self.base_info = BaseInfo(info, name, code)

    # 获取基金经理信息
    def set_manager_info(self):
        manager_info_html = requests.get(self.base_info.manager_html)
        manager_info_html.encoding='utf-8'
        soup = BeautifulSoup(manager_info_html.text, 'lxml')
        self.manager_info = ManagerInfo(soup)

    # 获取阶段涨幅信息
    def set_increase_info(self, all_info):
        info = all_info.find(name='li', attrs={'class': 'increaseAmount'})
        self.increase_info = IncreaseInfo(info)

    # 获取持仓股票信息
    def set_shares_info(self, all_info):
        info = all_info.find(name='li', attrs={'class': 'position_shares'})
        if info:
            self.shares_info = PositionInfo(info)
    # 获取持仓债券信息
    def set_bonds_info(self, all_info):
        info = all_info.find(name='li', attrs={'class': 'position_bonds'})
        if info:
            self.bonds_info = PositionInfo(info)

    def set_industry_info(self, code):
        # url = 'http://fundf10.eastmoney.com/hytz_' + code + '.html'
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36', 'Refer':'http://fundf10.eastmoney.com/hytz_000001.html'}
        url = 'http://api.fund.eastmoney.com/f10/HYPZ/?fundCode=000001&year=&callback=jQuery18304183865291790829_1608372149901&_=1608372149980'
        html = requests.get(url, headers)
        time.sleep(1)
        html.encoding='utf-8'
        soup = BeautifulSoup(html.text, 'lxml')
        infos = soup.find(name='div', attrs={'id': 'hypztable'})
        if infos:
            info = infos.find(name='div', attrs={'class': 'box'}.find(name='table'))
            self.industry_info = IndustryInfo(info)