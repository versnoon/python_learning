#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   test_bw_hr_salarys.py
@Time    :   2021/11/24 16:09:05
@Author  :   Tong tan 
@Version :   1.0
@Contact :   tongtan@gmail.com
'''

from src.salarys import bw_hr_salary
from src.salarys import salary_infos
from src.salarys import utils


class TestBwSalarys:

    def test_init_bw_folder(self):
        bw_hr_salary.init()
        p, departs, persons, gzs, jjs, banks, tax, gjjs = bw_hr_salary.load_data()
        df = bw_hr_salary.contact_info(
            gzs, jjs, banks=banks, persons=persons, tax=tax, gjjs=gjjs, departs=departs)
        period = p.get_period_info()
        df.to_excel('df.xlsx')
        # errs = salary_infos.validator(df)
        # if len(errs) > 0:

        # 输出汇总信息
        # salary_infos.export_all_errs(period, errs)
        # 根据税务单位输出数据
        # salary_infos.export_errs_by_depart_type(
        #     period, errs, departs.tax_departs(), utils.tax_column_name)
        # 根据显示单位输出数据
        # salary_infos.export_errs_by_depart_type(
        #     period, errs, departs.depart_dispaly_names())
        # sap = salary_infos.to_sap_frame(df)
