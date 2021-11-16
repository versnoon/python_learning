#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   data_read.py
@Time    :   2021/10/27 09:00:20
@Author  :   Tong tan 
@Version :   1.0
@Contact :   tongtan@gmail.com
'''


import os
import numpy as np
import pandas as pd


# 一次读取多少条记录
rows_per_one_read = 3000


def make_df_from_excel_files(
    file_root_path,
    period='',
    file_sub_path=[],
    file_name_prefix='',
    file_exts=['.xls', '.xlsx'],
    converters={},
):
    chunks = []
    err_paths = []
    file_dir = get_file_dir(file_root_path, period, file_sub_path)
    df = pd.DataFrame()
    if os.path.exists(file_dir):
        for file_name in os.listdir(file_dir):
            if file_name_validate(file_name, file_name_prefix, file_exts):
                file_path = get_file_path(
                    file_dir, file_name)
                file_df, err_path = make_df_from_excel(
                    file_path, converters)
                if not err_path and not file_df.empty:
                    chunks.append(file_df)
                else:
                    err_paths.append(err_path)
        if len(chunks) > 0:
            df = pd.concat(chunks, ignore_index=True)
    else:
        err_paths.append(file_dir)

    return df, err_paths


def group_by_columns(df, group_by_columns=[]):

    if not df.empty:
        if len(group_by_columns) > 0:
            df = df.groupby(group_by_columns, as_index=False)
            df = df.aggregate(np.sum)


def get_file_dir(file_root_path, period='', file_sub_path=[]):
    p = file_root_path
    if period:
        p = os.path.join(p, period)
    if len(file_sub_path) > 0:
        for s_p in file_sub_path:
            p = os.path.join(p, s_p)
    return p


def get_file_path(dir, file_name):
    return os.path.join(dir, file_name)


def file_name_validate(file_name, file_name_prefix, file_exts):
    return file_name_prefix_validator(file_name, file_name_prefix) and file_ext_validator(file_name, file_exts)


def file_name_prefix_validator(file_name, file_name_prefix):
    return file_name.startswith(file_name_prefix)


def file_ext_validator(file_name, file_exts):
    file_ext = get_file_ext(file_name)
    if file_ext in file_exts:
        return True
    return False


def make_df_from_excel(file_path, converters):
    df_chunks = pd.DataFrame()
    err_path = ''
    if os.path.exists(file_path):
        df_chunks = pd.read_excel(file_path, converters=converters)
        if df_chunks.empty:
            err_path = file_path
    else:
        err_path = file_path
    return df_chunks, err_path


def get_file_ext(file_path):
    """
    获取文件的后缀并统一抓换为小写
    """
    ext = os.path.splitext(file_path)
    if len(ext) == 0:
        return ""
    return ext[-1].lower()


def get_df_cell_value(df, column_name, row=0):
    key = column_name
    if not df[key].empty:
        return df[key].values[row]
    return ''
