from core import *

if __name__ == '__main__':
    routers_categories = ['modem-routers','wifi-routers','wifi-6']

    tem_index_url ='https://odinapi.asus.com.cn/recent-data/apiv2/SearchResult?SystemCode=asus&WebsiteCode=cn&SearchKey={search_key}&SearchType=support&SearchPDLine=networking-iot-servers&SearchPDLine2={category}&PDLineFilter=&TopicFilter=&CateFilter=&PageSize=10&Pages={page_index}&LocalFlag=0&siteID=www&sitelang=cn'
    save_path = '../data/ASUS'
    create_dir(save_path)
    search_keys = ['nas', '路由器']
    for search_key in search_keys:
        for category in tqdm(iterable=routers_categories, desc='categories'):
            if search_key == 'nas':
                category = 'wired-networking'
            for page_index in range(1, 10):
                index_url = tem_index_url.format(search_key=search_key,category=category, page_index=page_index)
                page = get_page(index_url)
                if page_index > 1:
                    last_page = get_page(tem_index_url.format(search_key=search_key, category=category, page_index=page_index - 1))
                    if last_page.content == page.content:
                        break

                pattern = '"ProductDownloadUrl":"([^"]+)"'
                links = get_links(page.content.decode(),pattern)
                models = [link.split('/')[-3] for link in links]
                template_url = 'https://www.asus.com.cn/support/api/product.asmx/GetPDBIOS?website=cn&model={model}&pdhashedid=&cpu=&pdid=99999&siteID=www&sitelang=cn'

                for model in tqdm(models, desc=category):
                    tmp_json = get_page(template_url.format(model=model)).json()
                    try:
                        for file in tmp_json['Result']['Obj'][0]['Files']:
                            save(file['DownloadUrl']['China'], save_path)
                    except Exception as e :
                        logging.error('In File: ASUS.py')
                        logging.error(e)





