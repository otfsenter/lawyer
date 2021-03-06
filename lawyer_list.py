import time
from pprint import pprint
import re

import requests
from bs4 import BeautifulSoup
from selenium import webdriver

import conf
from log import logger

from speciality import get_category

from speciality import strip_string

# url_category_root = 'http://www.64365.com'

# url_category_root 'http://www.64365.com/anhui/lawyer/page_%s.aspx'

DEFAULT_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'

headers = {
    'User-Agent': DEFAULT_USER_AGENT,
}


def get_lawyer_list(url_category_each, driver):
    """
    分页，每一页的
    :param url_category_each:
    :return:
    """

    logger.info(url_category_each)
    driver.get(url_category_each)
    time.sleep(1)

    driver.maximize_window()
    time.sleep(1)

    response = driver.page_source

    # response = requests.get(
    #     url=url_category_each,
    #     headers=headers).text

    soup = BeautifulSoup(response, 'html.parser')

    law_list = soup.find('ul', {'class': 'law-list box-bor1 mt20 sendsession-bigdata'})

    lis = law_list.find_all('li')

    url_lawyer_list = []
    for li in lis:
        div_fl = li.find('div', {'class': 'fl'})
        a_each_lawyer = div_fl.find('a')

        if a_each_lawyer:
            each_lawyer_href = strip_string(a_each_lawyer.get('href'))
            each_lawyer_text = strip_string(a_each_lawyer.get_text())
        else:
            each_lawyer_href = ''
            each_lawyer_text = ''

        url_lawyer_list.append([
            each_lawyer_href,
            each_lawyer_text
        ])

    return url_lawyer_list


def get_page_list(url_category_each):
    """
    1、如果中间有省略号，会忽略掉
    2、所以直接取最后一个数字，然后遍历范围内的所有页数
    3、页码包含'>'的直接去掉不要
    4、第一页的url就是变量url_category_each的值
    5、后面的页的url：url_category_each + 'page_%s.aspx' % str(num_page)

    :param url_category_each: 每个省份第一页的url
    :return: 每个省份所有页数的url
    """
    response = requests.get(
        url=url_category_each,
        headers=headers).text

    soup = BeautifulSoup(response, 'html.parser')

    page_list = soup.find('div', {'class': 'u-page'})

    if not page_list:
        return []

    as_ = page_list.find_all('a')

    url_page_list = []

    number_list = []
    for a in as_:
        if a:
            href_suffix = strip_string(a.get('href'))
            # text_page_origin = strip_string(a.get_text())
            text_page_number = strip_string(a.get_text())

            if text_page_number != '>':
                number_list.append(text_page_number)

    try:
        last_page_number = int(number_list[-1])
    except (ValueError, IndexError, TypeError):
        last_page_number = 1

    for num_page in range(1, last_page_number + 1):
        logger.info(num_page)

        href = url_category_each + 'page_%s.aspx' % str(num_page)

        if num_page == 1:
            href = url_category_each

        if href:
            logger.info(href)
            url_page_list.append(href)

    return url_page_list


def url_suffix2id(url_suffix):
    """
    '//www.64365.com/lawyer/1239347/'
    :param url_suffix:
    :return:
    """
    id_ = strip_string(url_suffix).split('/')[-2]

    re_result = re.match('\d+', id_)

    if re_result:
        return re_result.string
    else:
        return ''


def run():
    driver = webdriver.Chrome()

    # list_item_url_dict = get_category()

    url_shenhui_root = 'http://www.64365.com/%s/lawyer/'

    all_lawyer_dict = {}
    # for list_, item_url in list_item_url_dict.items():
    #     for item, url_category in item_url.items():
    #         url_category_each = url_category_root + url_category

    for shenhui in conf.shenhui:
        url_category_each = url_shenhui_root % shenhui

        logger.info(str(shenhui))

        time.sleep(2)

        # 获取每个专长下面的所有页面
        url_page_list = get_page_list(url_category_each)

        if url_page_list:
            # 从每个页面找所有律师
            for each_url_page in url_page_list:
                logger.info(each_url_page)

                time.sleep(1)

                url_lawyer_list_data = get_lawyer_list(each_url_page, driver)

                for url_lawyer_list in url_lawyer_list_data:

                    if url_lawyer_list and len(url_lawyer_list) > 1:
                        url = strip_string(url_lawyer_list[0])
                        lawyer = strip_string(url_lawyer_list[1])

                        if url and lawyer:
                            id_ = url_suffix2id(url)
                            all_lawyer_dict.setdefault(id_, lawyer)
                            logger.info('-'.join([
                                'lawyer0108',
                                str(id_),
                                str(lawyer)
                            ]))

            # {'//www.64365.com/lawyer/1239347/': '黄浩律师',
            #  '//www.64365.com/lawyer/1286074/': '兰易易律师',
            #  '//www.64365.com/lawyer/1405544/': '罗红律师' }

            # {'1239347': '黄浩律师',
            #  '1405544': '罗红律师',
            #  '1410121': '肖娟律师',

    driver.quit()

    pprint(all_lawyer_dict)
    # return


def main():
    run()


if __name__ == '__main__':
    main()
