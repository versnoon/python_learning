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


class TestBwSalarys:

    def test_init_bw_folder(self):
        bw_hr_salary.init()
        p, departs, persons, gzs, jjs, banks, tax = bw_hr_salary.load_data()
        df = bw_hr_salary.contact_info(
            gzs, jjs, banks=banks, persons=persons, tax=tax)
        period = p.get_period_info()
        errs = salary_infos.validator(df)
        if len(errs) > 0:
            # 输出汇总信息
            salary_infos.export_all_errs(period, errs)
            # 根据显示单位分别数据
            salary_infos.export_errs_by_display_depart(
                period, errs, departs.depart_dispaly_names())
        # sap = salary_infos.to_sap_frame(df)
