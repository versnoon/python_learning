#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   bw_hr_salary.py
@Time    :   2021/11/24 15:44:01
@Author  :   Tong tan 
@Version :   1.0
@Contact :   tongtan@gmail.com
'''
import os
import shutil
import pandas as pd

from src.salarys.utils import join_path, file_path_exists, make_folder_if_nessage, copy_file, gz_jj_dir, tax_dir, insurance_dir, result_dir, depart_file_name, gz_file_prefix, jj_file_prefix
from src.salarys.period import Period


def init():
    """
    根据期间初始化目录结构
    """
    p = load_period()
    period = p.get_period_info()
    init_folder_if_not_exists(period=period, folder_name=gz_jj_dir)
    init_folder_if_not_exists(period=period, folder_name=tax_dir)
    init_folder_if_not_exists(period=period, folder_name=insurance_dir)
    init_folder_if_not_exists(period=period, folder_name=result_dir)
    copy_depart_file_if_not_exists(p)
    clear(p)
    rename_to_standard(p)


def clear(period):
    dir = join_path([period.get_period_info(), result_dir])
    shutil.rmtree(dir)
    os.mkdir(dir)


def rename_to_standard(period: Period):
    # 工资奖金
    standard_file_name(period, gz_jj_dir)


def standard_file_name(period, foldername):
    dir = join_path([period.get_period_info()])
    if foldername:
        dir = join_path([period.get_period_info(), foldername])
    dir_files = os.listdir(dir)
    for file in dir_files:
        if file.lower().endswith('xls') or file.lower().endswith('xlsx'):
            file_path = join_path([dir, file])
            df = pd.read_excel(file_path, nrows=1)
            rename_and_copy_file(period, df, file_path)


def rename_and_copy_file(period, df, file_path):
    file_name, depart_info = get_file_name_info(df)
    dst_file_path = join_path(
        [period.get_period_info(), result_dir, f"{file_name}-{depart_info}.xlsx"])
    shutil.copyfile(file_path, dst_file_path)


def get_file_name_info(df):
    file_name = ""
    if is_gz(df.columns):
        file_name = gz_file_prefix
    elif is_jj(df.columns):
        file_name = jj_file_prefix
    depart_info = get_depart_info_from_departs(df)
    return file_name, depart_info


def get_depart_info_from_departs(df):
    depart_info = ""
    ds = df["所在机构"].str.split("\\")
    depart_info = ds.iloc[0][0]
    for d in ds.iloc[0]:
        if "总部" in d:
            depart_info = d
            break
    return depart_info


def is_gz(columns):
    return check_columnname_in_columns("养老保险个人额度", columns)


def is_jj(columns):
    return check_columnname_in_columns("基本奖金", columns)


def check_columnname_in_columns(column_name, columns):
    return column_name in columns


def init_folder_if_not_exists(period, folder_name):
    dir = join_path([period, folder_name])
    make_folder_if_nessage(dir)


def copy_depart_file_if_not_exists(p: Period):
    dir = join_path([p.get_period_info()])
    exists, dst_filepath = file_path_exists(dir, depart_file_name)
    if not exists:
        dir = join_path([p.get_pre_period_info()])
        exists, file_path = file_path_exists(dir, depart_file_name)
        if not exists:
            raise ValueError(f"获取{file_path}文件出错")
        # 复制文件
        copy_file(file_path, dst_filepath)


def load_period():
    return Period()
