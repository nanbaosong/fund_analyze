from base_data import * 
import json

class FundInfo(object):

    def __init__(self, all_info, name, code):
        self.set_base_info(all_info, name, code)
        self.set_manager_info()
        self.set_increase_info(all_info)
        self.set_shares_info(all_info)
        self.set_bonds_info(all_info)
        self.set_holding_info(code)
        self.set_special_info(code)

    # 获取基金基本信息
    def set_base_info(self, all_info, name, code):
        info = all_info.find(name='div', attrs={'class': 'infoOfFund'})
        self.base_info = BaseInfo(info, name, code)

    # 获取基金经理信息
    def set_manager_info(self):
        self.manager_info = ManagerInfo(None)
        manager_info_html = get_html_from_url_header(self.base_info.manager_html, headers)
        if manager_info_html:
            manager_info_html.encoding='utf-8'
            soup = BeautifulSoup(manager_info_html.text, 'lxml')
            self.manager_info = ManagerInfo(soup)

    # 获取阶段涨幅信息
    def set_increase_info(self, all_info):
        info = all_info.find(name='li', attrs={'class': 'increaseAmount'})
        self.increase_info = IncreaseInfo(info)

    # 获取持仓股票信息
    def set_shares_info(self, all_info):
        self.shares_info = PositionInfo(None)
        if self.base_info.fund_type != '货币型':
            info = all_info.find(name='li', attrs={'class': 'position_shares'})
            self.shares_info = PositionInfo(info)

    # 获取持仓债券信息
    def set_bonds_info(self, all_info):
        self.bonds_info = PositionInfo(None)
        if self.base_info.fund_type != '货币型':
            info = all_info.find(name='li', attrs={'class': 'position_bonds'})
            self.bonds_info = PositionInfo(info)

    # 获取基金的持有人信息
    def set_holding_info(self, code):
        self.holding_info = HoldingInfo(None)
        url = 'http://fundf10.eastmoney.com/FundArchivesDatas.aspx?type=cyrjg&code=' + code
        holding_info_html = get_html_from_url_header(url, headers)
        if holding_info_html:
            holding_info_html.encoding='utf-8'
            soup = BeautifulSoup(holding_info_html.text, 'lxml')
            if soup.find(name='tbody') and soup.find(name='tbody').find(name='tr'):
                info = soup.find(name='tbody').find(name='tr')
                self.holding_info = HoldingInfo(info)
    
    # 获取基金的特色数据（标准差，夏普比率）
    def set_special_info(self, code):
        self.special_info = SpecialInfo(None)
        url = 'http://fundf10.eastmoney.com/tsdata_' + code + '.html'
        special_info_html = get_html_from_url_header(url, headers)
        if special_info_html:
            special_info_html.encoding = 'utf-8'
            soup = BeautifulSoup(special_info_html.text, "lxml")
            if soup.find(name='div', attrs={'class':'detail'}) and soup.find(name='div', attrs={'class':'detail'}).find(name='table', attrs={'class':'fxtb'}):
                info = soup.find(name='div', attrs={'class':'detail'}).find(name='table', attrs={'class':'fxtb'})
                self.special_info = SpecialInfo(info)
                

