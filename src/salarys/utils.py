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
column_name_sep = '-'
column_name_suffix_sep = '_'
depart_info_sep = '\\'


depart_info_column_name = '机构'
code_info_column_name = '员工通行证'

tax_column_name = '税务机构'
depart_column_name = '单位名称'
depart_display_column_name = '单位显示名称'


def root_dir_() -> str:
    path = os.path.join(root_dir, test_dir)
    return path
