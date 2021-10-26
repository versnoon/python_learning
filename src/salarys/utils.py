#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   utils.py
@Time    :   2021/10/25 17:14:58
@Author  :   Tong tan 
@Version :   1.0
@Contact :   tongtan@gmail.com
'''

import os


# 文件跟目录
root_dir = r'D:\薪酬审核文件夹'
test_dir = 'test'
gz_jj_dir = '工资奖金数据'
tax_dir = '税务相关数据'

depart_sep = '-X-'


def root_dir_() -> str:
    path = os.path.join(root_dir, test_dir)
    return path
