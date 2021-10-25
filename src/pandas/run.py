#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   run.py
@Time    :   2021/10/25 15:47:06
@Author  :   Tong tan 
@Version :   1.0
@Contact :   tongtan@gmail.com
'''


import src.pandas.read_xls as prx


def load_excel_to_df():
    """
    加载相关数据并转为对应的dataframs
    """

    # 期间信息
    period_df = prx.make_df_from_excel_files(file_name_prefix='当前审核日期')
    period = period_str(prx.get_df_cell_value(
        period_df, '当前审核日期', '年'), prx.get_df_cell_value(period_df, '当前审核日期', '月'))

    # 审核机构信息
    depart_df = prx.make_df_from_excel_files(
        period=period, file_sub_path='', file_name_prefix='审核机构信息')

    #


def period_str(year, month):
    return "{:0>4d}{:0>2d}".format(int(year), int(month))
