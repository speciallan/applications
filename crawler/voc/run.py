#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Speciallan

import requests
import time
import re
import sys


def crawl_voc_list():

    site = 'https://www.51voa.com'

    total = 5000
    per_page = 50
    page = total // per_page

    all_article_urls = []

    # 获取所有文字链接
    for i in range(1, page+1):

        url = site + '/VOA_Standard_' + str(i) + '.html'
        content = requests.get(url)
        text = content.text

        list = re.findall(r'id="list"([\s\S]*)id="pagelist"', text)

        # 确保爬取到内容
        if len(list) > 0:
            list = list[0]
        else:
            break

        match = re.findall(r'<a href="(.*?)"', list)

        for article_sub_url in match:
            all_article_urls.append(site + article_sub_url)

        # 休息一下
        print(f'第{i}页文章列表爬取完毕')
        time.sleep(1)

    with open('voc_urls.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(all_article_urls))
        f.close()

    print('所有url爬取完毕')


def crawl_voc_article():

    from bs4 import BeautifulSoup

    # 爬取所有文章内容
    f = open('voc_urls.txt', 'r', encoding='utf-8')
    urls = f.readlines()
    f.close()

    for k, url in enumerate(urls):

        if k <= 1350:
            continue

        url = url.strip('\n')
        content = requests.get(url)
        text = content.text

        title = re.findall(r'class="title">([\s\S]*?)</div>', text)
        if len(title) > 0:
            title = title[0]
        else:
            title = re.findall(r'id="title">([\s\S]*?)</div>', text)
            if len(title) > 0:
                title = title[0]
            else:
                print(text)
                continue

        content = re.findall(r'class="Content">([\s\S]*)<div class="VOA_Content_Bottom"', text)
        if len(content) > 0:
            content = content[0]
        else:
            content = re.findall(r'id="content">([\s\S]*)<div id="Bottom_VOA"', text)
            if len(content) > 0:
                content = content[0]
            else:
                print(text)
                continue

        pattern = re.compile(r'<[^>]+>', re.S)

        title = pattern.sub('', title)
        content = pattern.sub('', content)
        content = content.rstrip('\n')

        # soup
        # content = BeautifulSoup(content, 'html.parser')
        # print(content.get_text())

        # print(title)
        # print(content)

        filename = str(k) + '_' + title.replace(' ', '_').replace(r'/', '_').replace('\\', '_') + '.txt'

        f = open('./data/' + filename, 'w', encoding='utf-8')
        f.write(content)
        f.close()

        print(f'第{k}篇文章爬取完毕')
        # time.sleep(0.1)

if __name__ == '__main__':
    # crawl_voc_list()
    crawl_voc_article()