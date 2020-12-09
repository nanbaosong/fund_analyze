from base_data_block_info import * 

class FundInfo(object):

    def __init__(self, all_info, name, code):
        base_info = all_info.find(name='div', attrs={'class': 'infoOfFund'})
        self.set_base_info(base_info, name, code)
        self.set_manager_info()
        increase_info = all_info.find(name='li', attrs={'class': 'increaseAmount'})
        self.set_increase_info(increase_info)
        pass

    def set_base_info(self, info, name, code):
        self.base_info = BaseInfo(info, name, code)

    def set_manager_info(self):
        manager_info_html = requests.get(self.base_info.manager_html)
        manager_info_html.encoding='utf-8'
        soup = BeautifulSoup(manager_info_html.text, 'lxml')
        self.manager_info = ManagerInfo(soup)

    def set_increase_info(self, info):
        self.increase_info = Increase(info)