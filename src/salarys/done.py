#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   done.py
@Time    :   2021/10/27 16:59:17
@Author  :   Tong tan
@Version :   1.0
@Contact :   tongtan@gmail.com
'''

import src.salarys.salary_infos as s_infos
import src.salarys.utils as utils
import pandas as pd


def load_data():
    # 加载数据
    period, ds, gzs, jjs, banks, jobs, persons = s_infos.load_data_to_frame()
    df = s_infos.merge_gz_and_jj(gzs, jjs)
    # s_infos.append_code_and_id_and_bank_and_tax_and_job(
    #     df, persons, banks, jobs)


def merge_salary_info():
    # 合并数据成一个dataframe
    pass


def app_export_column():
    # 增加导出字段
    pass


def export():
    # 输出
    pass


def merge(gz_infos, jj_infos, bank_infos, job_infos, person_infos, tax_infos):
    # 把相关数据合并
    # 合并工资奖金
    df = pd.merge(gz_infos.df, jj_infos.df, left_on=[s_infos.get_column_name(
        gz_infos.name, utils.code_info_column_name), s_infos.get_column_name(
        gz_infos.name, utils.tax_column_name), s_infos.get_column_name(
        gz_infos.name, utils.depart_display_column_name)], right_on=[s_infos.get_column_name(
            jj_infos.name, utils.code_info_column_name), s_infos.get_column_name(
            jj_infos.name, utils.tax_column_name), s_infos.get_column_name(
            jj_infos.name, utils.depart_display_column_name)], how='outer')
    df['']
    return df
