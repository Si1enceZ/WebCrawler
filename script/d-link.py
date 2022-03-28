from core import *
import time
if __name__ == '__main__':
    save_path = '../data/d_link'
    create_dir(save_path)
    index_url ='http://support.dlink.com.cn:9000/AllPro.aspx'
    index_page = get_page(index_url)

    pattern ='<a[ ]+href=[\'"]javascript:void\(0\);[\'"][ ]+class=[\'"]aRedirect[\'"][ ]+alt=[\'"]([^"]+)[\'"]>[^<]+路由器[^<]?</a>'
    models = get_links(index_page.content.decode(),pattern)

    tem_ver_url = 'http://support.dlink.com.cn:9000/ProductInfo.aspx?m={model}'
    for model in tqdm(models,desc="models"):
        ver_url = tem_ver_url.format(model=model)
        ver_page = get_page(ver_url)
        if ver_page == None:
            continue
        ver_pattern = '<option[^v]+value="([0-9]+)">'

        vers = get_links(ver_page.content.decode(),ver_pattern)
        if len(vers) == 0:
            continue
        vers = [int(ver) for ver in vers]

        tem_source_url = 'http://support.dlink.com.cn:9000/ajax/ajax.ashx?d={date}&action=productfile&lang=zh-cn&ver={ver}'
        tem_download_url = 'http://support.dlink.com.cn:9000/download.ashx?file={file_id}'
        for ver in vers:
            date = int(time.time()*1000)
            source_url = tem_source_url.format(date=date,ver=ver)

            source = get_page(source_url).json()

            for item in tqdm(source['item'],desc=model):
                if '固件' in item['file'][0]['name'] or '软件' in item['file'][0]['name']:
                    for file in item['file']:
                        file_id = file['id']
                        link = tem_download_url.format(file_id=file_id)
                        save(link,save_path)



