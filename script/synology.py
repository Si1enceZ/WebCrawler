from core import *
if __name__ == '__main__':
    save_path = '../data/synology'
    create_dir(save_path)
    pattern = '<a[ ]+href="([^"]+)"[ ]+rel="noreferrer noopener"'
    index_url = 'https://archive.synology.cn/download/Os'
    tem_url = 'https://archive.synology.cn'
    series = get_links(get_page(index_url).content.decode(),pattern)

    for s in tqdm(series[2:],desc='Series'):
        version_page = get_page(tem_url + s)
        versions = get_links(version_page.content.decode(),pattern)

        download_links = [tem_url + version for version in versions[3:]]
        Download(download_links,pattern,save_path)






