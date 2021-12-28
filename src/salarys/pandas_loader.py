#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   pandas_loader.py
@Time    :   2021/12/24 11:14:55
@Author  :   Tong tan 
@Version :   1.0
@Contact :   tongtan@gmail.com
'''

from src.salarys import data_read
from src.salarys import utils


def load_by_file_name_prefix(file_name_prefix, period='', sub_dirs=[], file_exts=['.xls', '.xlsx'], dtypes={}):
    return data_read.make_df_from_excel_files(
        utils.root_dir_(), period=period, file_sub_path=sub_dirs, file_name_prefix=file_name_prefix, file_exts=file_exts, dtypes={})


def load_by_file_name(file_name, period='', sub_dirs=[], dtypes={}):
    file_dir = data_read.get_file_dir(utils.root_dir_(), period, sub_dirs)
    file_path = data_read.get_file_path(file_dir, file_name)
    return data_read.make_df_from_excel(file_path, dtypes)
