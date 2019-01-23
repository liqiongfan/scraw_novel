import re
import os
import requests
from lxml import etree, html


def filter_tags(html_data):
    """
    过滤html标签
    :param html_data: 包含有html标签的文本字符串
    :return: 返回去掉了标签的字符串
    """
    dr = re.compile(r'<[^>]+>', re.S)
    dd = re.sub(dr, '', html_data)
    return dd


def get_index_content(page_url):
    """
    获取指定章节的内容
    :param page_url: 需要获取的章节的url
    :return: string 返回章节html
    """
    page_data = requests.get(page_url)
    page_html_data = etree.HTML(page_data.text)

    page_contents = page_html_data.xpath('//div[@id="nr1"]')[0]

    data = html.tostring(page_contents, method='text', encoding='unicode')
    return data


def write_content_to_file(file_name, file_data):
    """
    写入内容到文件中
    :param file_name: 文件名
    :param file_data: 文件内容
    :return:
    """
    file = open(file_name, 'a+')
    file.write(file_data)
    file.close()


def mkdir(path):
    """
    新建文件夹
    :param path: 路径
    :return:
    """
    folder = os.path.exists(path)

    if not folder:
        os.makedirs(path)
    else:
        print("目录:" + str(path) + "已存在")


def get_index(which_index, parent_dir):
    """
    获取第几部
    :param parent_dir:
    :param which_index: int
    :return: dict
    """
    url = "http://www.luoxia.com/guichui"
    data = requests.get(url)

    html_data = etree.HTML(data.text)
    indexs = html_data.xpath('//div[@class="book-list clearfix"][' + str(which_index) + ']/ul/li/a/text()')

    all_hrefs = html_data.xpath('//div[@class="book-list clearfix"][' + str(which_index) + ']/ul/li/a/@href')

    for key, val in enumerate(indexs):

        page_data = get_index_content(all_hrefs[key])

        write_content_to_file(str(parent_dir) + str('/') + str(val) + str('.txt'), page_data)


def get_all_indexs():
    """
    获取所有的章节
    :return: dict
    """
    url = "http://www.luoxia.com/guichui"
    data = requests.get(url)

    html_data = etree.HTML(data.text)
    indexs = html_data.xpath('//div[@class="title clearfix"]/h3/a/text()')

    for key, index in enumerate(indexs):
        mkdir(index)
        get_index(key+1, index)


get_all_indexs()
