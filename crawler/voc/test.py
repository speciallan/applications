#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Speciallan

from bs4 import BeautifulSoup

str = '<div class="111"><a><img src="222">ttttt</a></div><div class="111"><a><img src="222">ttttt</a></div><div class="111"><a><img src="222">ttttt</a></div>'
soup = BeautifulSoup(str, 'lxml')
text = soup.get_text()
result = soup.find('div')
results = soup.find_all('div')
# result = result.a.img
r = []
for i in results:
    r.append(i.a.img['src'])

# print(text)
print(results)
print(r)