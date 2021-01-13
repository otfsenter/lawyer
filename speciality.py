import time

import requests
from bs4 import BeautifulSoup
from log import logger

url_map = 'http://www.64365.com/about/map.aspx'

DEFAULT_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'

headers = {
    'User-Agent': DEFAULT_USER_AGENT,
}


def strip_string(text, replace_str=None):
    if replace_str and isinstance(replace_str, str):
        return str(text).strip().replace(replace_str, '')

    return str(text).strip()


def get_category():
    # driver = webdriver.Chrome()
    #
    # driver.get(url_map)
    # time.sleep()
    # response = driver.page_source

    response = requests.get(url=url_map, headers=headers).text

    # print(response)

    soup = BeautifulSoup(response, 'html.parser')

    div_maps_list = soup.find_all('div', {'class': 'map-list'})

    list_item_url_dict = {}

    for each_map in div_maps_list:
        each_map_text = each_map.get_text()

        if '按专长找律师' in each_map_text and '按专长找律师电话' not in each_map_text:

            lis = each_map.find_all('li')

            for li in lis:
                span_category = strip_string(li.find('span').get_text(), ':')

                # print('类别：', span_category)

                as_ = li.find_all('a')

                for a in as_:
                    a_href = strip_string(a.get('href'))
                    a_text = strip_string(a.get_text())

                    list_item_url_dict.setdefault(span_category, {}).setdefault(a_text, a_href)

                    # print('url: ', a_href)
                    # print('细分类别: ', a_text)
                #
                # print('=============================================================================================')

    # '互联网纠纷': {'电子商务纠纷': '/hlwjf/dzswjf/',
    #            '网络诈骗纠纷': '/hlwjf/wlzpjf/',
    #            '网络金融纠纷': '/hlwjf/wljrjf/'},
    #  '交通事故': {'交通事故处理': '/jiaotong/jtsgjf/',
    #           '交通事故类鉴定': '/jiaotong/jtsgjd/',
    return list_item_url_dict

def main():
    a = get_category()
    logger.log(str(a))


if __name__ == '__main__':
    main()
