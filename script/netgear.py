from core import *

if __name__ == '__main__':
    save_path = '../data/netgear'
    create_dir(save_path)

    index_url = 'http://support.netgear.cn/download.asp'
    index_page = get_page(index_url)

    product_pattern = '<option[ ]+value="([^"]+)"[ ]+>'
    ids = get_links(index_page.text, product_pattern)
    tem_download_url = 'http://support.netgear.cn/'
    links = [tem_download_url + id for id in ids]

    download_pattern = '<a href="([^"]+)">Version'

    for link in tqdm(links):
        download_page = get_page(link)
        try:
            download_links = get_links(download_page.text, download_pattern)
        except Exception as e:
            print(e)
            print(link)
            continue

        if download_links is not None:
            for download_link in download_links:
                download_link = tem_download_url + download_link
                try:
                    save(download_link, save_path)

                except Exception as e:
                    print(e)
                    continue
        else:
            print(f'Can\'t find the download link in page: {link}')

