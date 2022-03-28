from core import *
if __name__ == '__main__':
    index_url = 'https://www.tenda.com.cn/download/cata-11.html'
    save_path = '../data/Tenda'
    create_dir(save_path)
    page = get_page(index_url)

    pattern = '<a[ ]+href="([^"]+)"[ ]+title="[^"]+"[ ]+target="_blank">'
    links = get_links(page.content.decode(), pattern)
    links = ['http:' + link for link in links]

    Download(links, '<a[ ]+href="(https://[^"]+.zip)"[ ]+data-lang="[^"]+"[ ]+target="_blank">',save_path)
