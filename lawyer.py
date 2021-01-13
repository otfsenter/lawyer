import requests
from bs4 import BeautifulSoup
from log import logger
from speciality import strip_string

url_info = 'http://www.64365.com/lawyer/%s/info/'

# {'1239347': '黄浩律师',
#  '1405544': '罗红律师',
#  '1410121': '肖娟律师',

DEFAULT_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'

headers = {
    'User-Agent': DEFAULT_USER_AGENT,
}


def banner1(soup):
    """
    姓名: name
    地点: location
    公司名字: company
    专业领域: skill
    解答咨询: question_and_answer
    获得点赞: like
    获得好评: comment
    综合得分: score
    联系方式: phone_number
    简介: brief_introduction

    :param soup:
    :return:
    """
    result_name_lr = soup.find('div', {'class': 'lr'}).get_text().strip()

    location_inf = soup.find('div', {'class': 'inf'})
    result_location = location_inf.find('i').get_text().strip().replace('"', '')
    result_company = location_inf.find('span').get_text().strip()

    skill = soup.find('div', {'class': 'skill'})
    skill_spans = skill.find_all('span')
    skill_spans_list = []
    for skill_span in skill_spans:
        skill_span_text = skill_span.get_text().strip()
        skill_spans_list.append(skill_span_text)
    result_skill = ','.join(skill_spans_list)

    question_and_answer_h110 = soup.find('div', {'class': 'h110'})
    question_and_answer_fr = question_and_answer_h110.find('div', {'class': 'fr'})
    result_phone_number = question_and_answer_fr.find('span').get_text().strip()

    question_and_answer_num = question_and_answer_h110.find('ul', {'class': 'num'})
    question_and_answer_num_ns = question_and_answer_num.find_all('li', {'class': 'n'})
    qaann_dict = {}
    for qaann in question_and_answer_num_ns:
        qaann_text = qaann.find('span').get_text().strip()
        qaann_num = qaann.find('p', {'class': 'f-num'}).get_text().strip()
        qaann_dict.setdefault(qaann_text, qaann_num)

    return [
        result_name_lr,
        result_location,
        result_company,
        result_skill,
        qaann_dict.get('解答咨询', ''),
        qaann_dict.get('获得点赞', ''),
        qaann_dict.get('获得好评', ''),
        qaann_dict.get('综合得分', ''),
        result_phone_number,
        ''
    ]


def banner4(soup):
    div_data = soup.find('div', {'class': 'data'})

    left_fl = div_data.find('div', {'class': 'left fl'})
    result_name_location = left_fl.find('div', {'class': 'lr'})
    result_name = result_name_location.find('h1').get_text().strip()
    result_location = result_name_location.find('span').get_text().strip()

    skill = left_fl.find('div', {'class': 'skill'})
    skill_spans = skill.find_all('span')
    skill_spans_list = []
    for skill_span in skill_spans:
        skill_span_text = skill_span.get_text().strip()
        skill_spans_list.append(skill_span_text)
    result_skill = ','.join(skill_spans_list)

    question_and_answer_num = left_fl.find('ul', {'class': 'num clearfix'})
    question_and_answer_num_ns = question_and_answer_num.find_all('li', {'class': 'n'})
    qaann_dict = {}
    for qaann in question_and_answer_num_ns:
        qaann_text = qaann.find('span').get_text().strip()
        qaann_num = qaann.find('p', {'class': 'f-num'}).get_text().strip()
        qaann_dict.setdefault(qaann_text, qaann_num)

    r_touch_fr = div_data.find('div', {'class': 'r-touch fr'})
    result_phone_number = r_touch_fr.find('span', {'class': 'tel f-num'}).get_text().strip()

    result_company = ''
    result_txt = ''

    return [
        result_name,
        result_location,
        result_company,
        result_skill,
        qaann_dict.get('解答咨询', ''),
        qaann_dict.get('获得点赞', ''),
        qaann_dict.get('获得好评', ''),
        qaann_dict.get('综合得分', ''),
        result_phone_number,
        result_txt,
    ]


def banner2(soup):
    ban_txt = soup.find('div', {'class': 'ban-txt'})

    result_name = ban_txt.find('div', {'class': 'lawyer'}).find('h1').get_text().strip()

    result_location = ban_txt.find('div', {'class': 'diqu'}).get_text().strip().replace('"', '')

    skill = ban_txt.find('div', {'class': 'skill'})
    skill_spans = skill.find_all('span')
    skill_spans_list = []
    for skill_span in skill_spans:
        skill_span_text = skill_span.get_text().strip()
        skill_spans_list.append(skill_span_text)
    result_skill = ','.join(skill_spans_list)

    result_txt = ban_txt.find('div', {'class': 'txt'}).get_text().strip().replace('"', '')

    result_phone_number = ban_txt.find('div', {'class': 'tel-bar'}).find('span').get_text().strip()

    qaann_dict = {}
    result_company = ''

    return [
        result_name,
        result_location,
        result_company,
        result_skill,
        qaann_dict.get('解答咨询', ''),
        qaann_dict.get('获得点赞', ''),
        qaann_dict.get('获得好评', ''),
        qaann_dict.get('综合得分', ''),
        result_phone_number,
        result_txt,
    ]


def get_banner(soup):
    for i in range(1, 6):
        div_banner = soup.find('div', {'class', 'banner-%s' % str(i)})
        if div_banner:

            if i == 1:
                # ['张少于律师', '', '湖南·长沙', '非诉讼类,税务类纠纷,行政类', '-', '-', '-', '', '073-1-84-118636', '']
                banner_list = banner1(soup)
            elif i == 2:
                # ['宋磊律师', '广东·深圳', '', '婚姻家庭', '', '', '', '', '135-1016-9788', '宋磊，现为北京市盈科（深圳）律师事务所家族法律事务中心专职律师，曾在某市中级人民法院婚姻家事庭工作长达五年时间。宋磊律师曾长期工作于法院系统，专职参与婚姻家事、...']
                banner_list = banner2(soup)
            elif i == 4:
                # ['广东深谋律师事务所', '广东-深圳', '', '刑事辩护,公司经营,婚姻家庭', '475', '-', '-', '', '134-3055-9335', '']
                banner_list = banner4(soup)
            else:
                banner_list = [''] * 10
            return banner_list
    return [''] * 10


def get_detail(soup):
    """
    律师信息

联系方式-联系电话
联系方式-微信
联系方式-邮箱
联系方式-联系地址

执业信息-执业律所
执业信息-律所规模
执业信息-职务
执业信息-执业证号
执业信息-团队描述

教育背景-最高学历
教育背景-毕业院校
教育背景-所学专业

个人资料-性别
个人资料-年龄
个人资料-民族
个人资料-属相
个人资料-星座
个人资料-故乡
个人资料-家庭
个人资料-语音

更多信息-政治派别
更多信息-政治职务
更多信息-交通工具
更多信息-兴趣爱好

* 成长经历:
* 时段
* 经历
* 职务

* 教育背景:
* 顾问经历
* 时段
* 顾问单位
* 单位性质

    :param soup:
    :return:
    """
    pass


def info_auth(url):
    response = requests.get(
        url=url,
        headers=headers).text

    soup = BeautifulSoup(response, 'html.parser')

    banner_list = get_banner(soup)

    if not any(banner_list):
        get_detail(soup)


def main():
    url = url_info % '733897'
    # http://www.64365.com/lawyer/733896/info/
    # banner-1
    a = ['张少于律师', '湖南·长沙湖南天恒健律师事务所', '非诉讼类税务类纠纷行政类',
         '解答咨询-', '获得点赞-', '获得好评-', '综合评分-', '073-1-84-118636', '在线咨询']

    # http://www.64365.com/lawyer/5705351/info/
    # banner-2

    # http://www.64365.com/lawyer/8394206/info/
    # banner-4
    b = ['团队成员：', '暂未关联律师', '广东深谋律师事务所', '广东-深圳', '刑事辩护公司经营婚姻家庭',
         '解答咨询475', '获得点赞-', '获得好评-', '综合评分-', '在线咨询',
         '134-3055-9335', '来电请说明来自律图', '(服务时间：09：00~21：00)']

    # http://www.64365.com/lawyer/8394206/info/

    print(url)
    info_auth(url)


if __name__ == '__main__':
    main()
