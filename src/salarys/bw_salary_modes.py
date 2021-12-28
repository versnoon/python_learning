#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   bw_salary_modes.py
@Time    :   2021/12/24 09:39:30
@Author  :   Tong tan
@Version :   1.0
@Contact :   tongtan@gmail.com
'''


import pandas as pd

from src.salarys import errs
from src.salarys import utils
from src.salarys import pandas_loader

# pandas
loader = pandas_loader


# —————————————————————————————————————— 审核期间信息 ——————————————————————————————————————
period_info = {'year': -1, 'month': -1}


def period_file_name():
    return f'{utils.period_file_name}.xls'


def load_period_info():
    data, _ = loader.load_by_file_name(
        period_file_name())
    if data.empty:
        raise errs.NOT_FOUND_PERIOD_ERR
    row_nums = data.shape[0]
    if row_nums == 1:
        period_info['year'] = data.iloc[[0], [0]].values[0][0]
        period_info['month'] = data.iloc[[0], [1]].values[0][0]


def period():
    year = period_info['year']
    month = period_info['month']
    return "{:0>4d}{:0>2d}".format(year, month)


def pre_period():
    year = period_info['year']
    month = period_info['month']
    if month != 1:
        return "{:0>4d}{:0>2d}".format(year, month-1)
    else:
        return "{:0>4d}{:0>2d}".format(year - 1, 12)

# —————————————————————————————————————— 审核机构信息 ——————————————————————————————————————


depart_df = pd.DataFrame()


def load_depart_info():
    data, _ = loader.load_by_file_name(utils.depart_file_name)
    if data.empty:
        raise errs.NOT_FOUND_PERIOD_ERR
    depart_df = data
