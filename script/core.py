import requests
import re
import random
from tqdm import tqdm
import os
import logging
import json

ua_list = [
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0)',
    'AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
    'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
    'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
    # 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    # 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)',
    'Chrome/99.0.4844.74 Safari/537.36 Edg/99.0.1150.52 '
]
file_types = ['apk', 'pdf', 'exe']


def create_dir(directory_name: str):
    """
    创建文件夹
    :param directory_name: 文件夹名称
    :return: None
    """
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(lineno)d - %(funcName)s - %(message)s"
    DATE_FORMAT = "%Y/%m/%d %H:%M:%S"
    name = directory_name.split('/')[-1]
    f = open('log/' + name + '.log', 'a', encoding='utf-8')
    f.close()

    logging.basicConfig(filename='log/' + name + '.log', level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT)
    try:
        os.makedirs(directory_name)
        logging.debug(f'Succeed in creating directory: {directory_name}')
    except FileExistsError:
        logging.debug(f'Directory {directory_name} already exists!')
        return


def get_page(url: str, headers=None):
    """
    通过get打开指定url的页面
    :param headers: 文件头
    :param url: 需要get的页面地址
    :return: get后的页面
    """

    if headers is None:
        headers = {}
    if headers.get('User-Agent') is None:
        headers['User-Agent'] = random.choice(ua_list)
    try_times = 10
    for i in range(try_times):
        try:
            html = requests.get(url=url, headers=headers)
            return html
        except Exception as e:
            if e == ConnectionError:
                logging.debug(f'The {i} times can\'t open the page: {url} in function {get_page.__name__}')
                continue
            else:
                logging.error(f'In Function: get_page({url})')
                logging.error(e)

                return None
    else:
        logging.error(f'After Ten tries,can\'t open the page: {url} in function {get_page.__name__}')


def get_bios(url: str):
    """
    根据BIOS下载链接获取BIOS固件，stream=True
    :param url: bios下载链接
    :return: bios链接的requests.models.Response
    """

    ua = {'User-Agent': random.choice(ua_list)}
    for i in range(10):
        try:
            html = requests.get(url=url, stream=True, headers=ua)

            return html
        except Exception as e:
            if e == ConnectionError:
                logging.debug(f'The {i} times can\'t get the bios: {url} in function {get_page.__name__}')
                continue
            else:
                logging.error(f'In Function: get_bios({url})')
                logging.error(e)
                return None
    else:
        print(f'Can\'t get the bios: {url} in function {get_page.__name__}')


def get_links(text: str, pattern: str):
    """
    根据正则匹配式来获取页面内所有的链接
    :param text: 页面content
    :param pattern: 正则表达式
    :return: 页面匹配的所有链接
    """
    find = re.compile(pattern, re.S)
    return find.findall(text)


def test_save(url, path):
    tmp = {"url": url, "name": url.split('/')[-1]}
    with open(path + '/' + path.split('/')[-1] + '.json', 'a', encoding='utf-8') as file:
        file.write(json.dumps(tmp) + '\n')
    logging.info("Succeed in sava file");


def save(url, path):
    """
    保存单个文件
    :param url: 下载链接
    :param path: 保存路径
    :return: None
    """
    file_type = url.split('.')[-1]
    if file_type in file_types or file_type is None:
        return
    test_save(url, path)
    # name = url.split('/')[-1]
    # if not os.path.exists(name):
    #     file_internet = get_bios(url)
    #     content_size = int(int(file_internet.headers['Content-Length']) / (1024 * 1024) + 0.5)
    #
    #     with open(path + '/' + name, 'wb') as file_local:
    #         print(f'File {name} total size is about:', content_size, 'MB. starting save...')
    #         logging.debug(f'Saving File {name}..')
    #         try:
    #             for data1 in tqdm(iterable=file_internet.iter_content(1024 * 1024), total=content_size, desc=name,
    #                          unit='MB'):
    #                 file_local.write(data1)
    #             else:
    #                 logging.debug(f'Succeed in saving file {name}')
    #         except Exception as e:
    #             logging.error(f'In function save')
    #             logging.error(e)


def Download(links: list, pattern: str, path: str):
    """
    对所有下载页面进行下载
    :param links: 所有需要下载页面的链接列表
    :param pattern: 获取下载链接的正则表达式
    :param path: 保存路径文件夹名称
    :return: None
    """
    for link in tqdm(links):
        download_page = get_page(link)
        download_links = get_links(download_page.content.decode(), pattern)
        if download_links is not None:
            for download_link in download_links:
                try:
                    save(download_link, path)
                except Exception as e:
                    logging.error('In function Download')
                    logging.error(e)
                    continue
        else:
            logging.error(f'Can\'t find the download link in page: {link}')


def save_page(page: requests.models.Response, encoding='utf-8'):
    with open('tmp.html', 'w', encoding=encoding) as f:
        f.write(page.content.decode(encoding=encoding))


def test_page(url: str, encoding='utf-8', headers=None):
    if headers is None:
        headers = {}
    f = get_page(url, headers)
    save_page(f, encoding)
