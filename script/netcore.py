from core import *
if __name__ == '__main__':
    save_path = '../data/netcore'
    create_dir(save_path)

    tem_url = 'http://www.netcoretec.com/'
    tem_index_url = 'http://www.netcoretec.com/portal/list/index/id/12.html?id=12&page={page}'

    for i in range(1,7):
        page = get_page(tem_index_url.format(page=i))
        index_pattern = '<a[ ]+class="btn"[ ]+target="_blank" href="([^"]+)">'
        links = get_links(page.content.decode(), index_pattern)
        if len(links)==0:
            index_pattern='<a[ ]+class="tag"[ ]+href="([^"]+)">'
            links = get_links(page.content.decode(),index_pattern)
        links = [tem_url+link for link in links]

        download_pattern = '<input[ ]+type="checkbox"[ ]+class="load_check[ ]+check_item"[ ]+file_url="([^"]+)"[ ]+>'
        for link in tqdm(links,desc=f'page{i}'):
            download_page = get_page(link)
            download_links = get_links(download_page.content.decode(), download_pattern)
            if download_links is not None:
                download_links = [tem_url+link for link in download_links]
                for download_link in download_links:
                    try:
                        save(download_link, save_path)
                    except Exception as e:
                        logging.error('In function Download')
                        logging.error(e)
                        continue
            else:
                logging.error(f'Can\'t find the download link in page: {link}')
