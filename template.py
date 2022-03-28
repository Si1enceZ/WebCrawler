import csv
import json
import os

import requests


def make_csv(crawl_dict):
    """
    书写csv文件

    :param crawl_dict: 最终爬取的字典
    :return:
    """
    with open("./data/laptop_data.csv", 'w+', encoding='utf-8') as f:
        f.write(u'\ufeff')  # 处理Excel打开乱码
        # 设置csv文件头
        csv_write = csv.writer(f)
        csv_head = ['系列', '型号']
        csv_write.writerow(csv_head)
        for k in crawl_dict.keys():
            for model in crawl_dict[k]:
                csv_data = [k, model]
                csv_write.writerow(csv_data)

            csv_break = ['', '']
            csv_write.writerow(csv_break)


if __name__ == '__main__':
    id_dict = {}
    final_dict = {}

    # 修改请求头, 伪装成浏览器访问
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/71.0.3578.98 Safari/537.36",
    }

    product_url = "https://www.asus.com.cn/support/api/product.asmx/GetPDLevel?website=cn&type=1&typeid=155" \
                  "&productflag=0 "

    try:
        product = requests.get(product_url, headers=headers, timeout=(60, 60))
        product.raise_for_status()
        product.encoding = "UTF-8"

        product_text = product.text
        product_dict = json.loads(product_text)
        products = product_dict['Result']['ProductLevel']['Products']['Items']  # 获得产品系列列表

        for item in products:
            # 循环列表中每一项，每一项为一个dict，dict中第一项为value值，第二项为系列的name值
            id_dict[item['Id']] = item['Name']
            final_dict[item['Name']] = []

        for k in id_dict.keys():
            # 循环id字典中的每一项，其中k为value值，用于访问链接，v为系列名字，用户添加数据至final_dict中的列表
            model_url = 'https://www.asus.com.cn/support/api/product.asmx/GetPDLevel?website=cn&type=2&typeid=' + k + \
                        '&productflag=1 '
            try:
                model = requests.get(model_url, headers=headers, timeout=(60, 60))
                model.raise_for_status()
                model.encoding = "UTF-8"
                model_text = model.text
                model_dict = json.loads(model_text)
                models = model_dict['Result']['Product']  # 获取型号列表

                for item in models:
                    final_dict[id_dict[k]].append(item['PDName'])
            except:
                print("页面爬取失败！")
                break

        print("爬取成功，正在写入文件！")
        if not os.path.exists("./data"):
            # 如果文件夹data不存在，创建文件夹，并且书写文件，否则直接书写文件
            os.makedirs("./data")
            make_csv(final_dict)
        else:
            make_csv(final_dict)

        print("文件写入成功！")
    except:
        print("页面爬取失败！")
