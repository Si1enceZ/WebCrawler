from core import *

if __name__ == '__main__':
    path = '../data/hikvision'
    create_dir(path)

    index_urls = [ 'https://www.hikvision.com/content/hikvision/cn/support/Downloads/Device-upgrade-package/jcr:content/root/responsivegrid/article_listing_copy.download-pages.json','https://www.hikvision.com/content/hikvision/cn/support/Downloads/Universal-Server-Driver/jcr:content/root/responsivegrid/article_listing_copy.download-pages.json',]
    tem_page = 'https://www.hikvision.com'
    download_pattern = 'data-link="([^"]+)" btn-link="btn-link" target="_self"'

    for index_url in index_urls:
        page_links = []
        index_json = get_page(index_url).json()
        for tmp in index_json['content']['data']['dataArray']:
            try:
                page_links.append(tem_page+tmp['newsUrl'][:-5])
            except:
                continue

        for link in tqdm(page_links):
            download_page = get_page(link)
            if link == 'https://www.hikvision.com/cn/support/Downloads/Device-upgrade-package/upgrade-package/':
                download_links = get_links(download_page.content.decode(), '<a[ ]+href="([^"]+)">点击下载</a>')
            else:
                download_links = get_links(download_page.content.decode(), download_pattern)
            if download_links is not None:
                for download_link in download_links:
                    save(tem_page + download_link, path)
            else:
                print(f'Can\'t find the download link in page: {link}')


