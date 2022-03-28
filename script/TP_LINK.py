from core import *
if __name__ == '__main__':
    save_path = '../data/TP_LINK'
    create_dir(save_path)

    tem_url = 'https://service.tp-link.com.cn/download?classtip=software&p={}&o=0'
    tem_page_url = 'https://service.tp-link.com.cn'
    for i in tqdm(range(1,204),desc='Page'):
        index_url = tem_url.format(i)
        index_page = get_page(index_url)

        download_page_pattern = '<a[ ]+href="(/detail_download_[0-9]+.html)"'
        download_page_links = get_links(index_page.content.decode(),download_page_pattern)
        download_page_links = [tem_page_url + link for link in download_page_links]

        download_pattern = 'href="(https://[^"]+[rarzip])"'
        Download(download_page_links,download_pattern,save_path)

