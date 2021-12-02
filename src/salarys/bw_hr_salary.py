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

from src.salarys.utils import join_path, file_path_exists, make_folder_if_nessage, copy_file, gz_jj_dir, tax_dir, insurance_dir, result_dir, depart_file_name, gz_file_prefix, jj_file_prefix, code_info_column_name, person_id_column_name, tax_column_name, depart_display_column_name
from src.salarys.period import Period
from src.salarys.depart import Departs
from src.salarys.salary_infos import SalaryBanks, SalaryBaseInfo, SalaryGzs, SalaryJjs, SalaryTaxs, SalaryGjj, get_column_name, merge_gz_and_jj, contact_bank_info, contact_tax_info


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
    # rename_to_standard(p)


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


def load_depart(period):
    return Departs(period)


def load_person_info(period):
    return BwSalaryPersons(period)


def load_data():
    p = load_period()
    period = p.get_period_info()
    departs = load_depart(period=period)
    persons = load_person_info(period=period)
    gzs = SalaryGzs(period, departs)
    jjs = SalaryJjs(period, departs)
    banks = SalaryBanks(period, departs)
    tax = SalaryTaxs(period, departs.tax_departs())
    gjjs = SalaryGjj(period, departs)
    return p, departs, persons, gzs, jjs, banks, tax, gjjs


def contact_info(gzs, jjs, banks=None, persons=None, tax=None, gjjs=None, departs=None):
    df = merge_gz_and_jj(gzs, jjs)
    df = contact_bw_person_info(df, persons)
    df = contact_bank_info(df, banks)
    df = contact_tax_info(df, tax)
    df = contact_gjj_info(df, gjjs)
    df = contact_gjj_validate(df, departs)
    return df


def contact_bw_person_info(df, persons):
    if persons.df.empty:
        return df
    id_df = persons.df[[code_info_column_name, tax_column_name, get_column_name(
        persons.name, person_id_column_name), get_column_name(
        persons.name, "手机号码"), get_column_name(
        persons.name, "人员类型"), get_column_name(
        persons.name, "在职状态"), get_column_name(
        persons.name, "聘用形式"), get_column_name(
        persons.name, "岗位"), get_column_name(
        persons.name, "标准岗位层级"), get_column_name(
        persons.name, "岗位族群（主）")]]
    return pd.merge(df, id_df, on=[code_info_column_name, tax_column_name], how='left')


def contact_gjj_info(df, gjjs):
    if gjjs.df.empty:
        return df
    gjj_column = get_column_name(SalaryGjj.name, '公积金方案')
    gjj_df = gjjs.df[[code_info_column_name, tax_column_name, gjj_column]]
    return pd.merge(df, gjj_df, on=[
        code_info_column_name, tax_column_name], how='left')


def contact_gjj_validate(df, departs):
    df['公积金验证'] = df.apply(lambda x: departs.get_gjj_fangan(
        x[tax_column_name], x[get_column_name(SalaryGjj.name, '公积金方案')], x[depart_display_column_name]), axis=1)
    return df.copy()


class BwSalaryPersons(SalaryBaseInfo):
    """
    发薪人员信息
    """
    name = '人员信息导出结果'

    def __init__(self, period) -> None:
        super().__init__(period)
        self.name = '人员信息导出结果'
        super().get_infos()
