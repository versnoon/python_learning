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


def done():
    # 加载数据
    period, departs, gzs, jjs, banks, jobs, persons, tax = s_infos.load_data_to_frame()
    # 合并数据
    # banks.df.to_excel('bank.xlsx')
    df = s_infos.contact_info(gzs, jjs, banks, jobs, persons, tax)
    # 验证数据
    errs = s_infos.validator(df)
    if len(errs) > 0:
        # 输出汇总信息
        s_infos.export_all_errs(period, errs)
        # 根据显示单位分别数据
        s_infos.export_errs_by_display_depart(
            period, errs, departs.depart_dispaly_names())
    # 输出各类数据
    else:
        s_infos.export(gzs, jjs, df)
