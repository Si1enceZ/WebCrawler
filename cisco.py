from script.core import *


def get_token(page):
    ts_pattern = 'var ts = "([a-zA-Z0-9]+)"'
    tkn_pattern = 'var tkn = "([a-zA-Z0-9]+)"'
    ts = get_links(page.content.decode(), ts_pattern)[0]
    tkn = get_links(page.content.decode(), tkn_pattern)[0]

    return [ts, tkn]


if __name__ == '__main__':
    path = '../data/cisco'
    create_dir(path)
    index_url = 'https://software.cisco.com/download/home'
    index_page = get_page(index_url)
    # 从索引页面获取ts和tkn两个请求参数
    ts,tkn = get_token(index_page)

    # 所有列表内的值
    source_page = get_page('https://software.cisco.com/services/catalog/v1/products?mdfid=268437899&ts='+ts,headers={'Authorization': 'Bearer '+tkn})
    tem_download_page = 'https://software.cisco.com/download/home/{mdfid}}/type'
    tem_type_url = 'https://software.cisco.com/services/catalog/v1/softwareTypes?mdfid={mdfid}&ts={ts}'
    mdfid_pattern = '"mdfId":"([0-9]+)","metaClass":"[^"]+","mdfConcept":"[^"]+","parentMdfId":"[0-9]+","leafNodeFlag":"Y"'
    mdfids = get_links(source_page.content.decode(),mdfid_pattern)


    # TODO 固件包似乎需要购买产品才能进行下载



