#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   req.py
@Time    :   2021/04/02 13:32:19
@Author  :   Tong tan 
@Version :   1.0
@Contact :   tongtan@gmail.com
'''


import requests


if __name__ == '__main__':

    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"}

    r = requests.get(
        r'https://cas.baogang.info/cas/login?loginType=mixLogin&userSystem=ehr&cssName=bsts&redirectUrl=http://ehr.baogang.info/hs/index.jsp', headers=headers)
    print(r.status_code)
    print(r.text)
