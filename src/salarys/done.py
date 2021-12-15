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
import src.salarys.bw_hr_salary as b_infos
import src.salarys.utils as utils


def done():
    # 加载数据
    period, departs, gzs, jjs, banks, jobs, persons, tax, taxOne, gjjs = s_infos.load_data_to_frame()

    # 合并数据
    # banks.df.to_excel('bank.xlsx')
    df = s_infos.contact_info(gzs=gzs, jjs=jjs, banks=banks, jobs=jobs,
                              persons=persons, tax=tax, taxOne=taxOne, gjjs=gjjs, departs=departs)
    # 验证数据
    errs = s_infos.validator(df)
    if len(errs) > 0:
        # 输出汇总信息
        s_infos.export_all_errs(period, errs)
        # 根据显示单位分别数据
        s_infos.export_errs_by_depart_type(
            period, errs, departs.depart_dispaly_names())
    # 输出各类数据
    # else:
    #     s_infos.export(gzs, jjs, df)
    # s_infos.to_sap_frame(df)
    tax_res = b_infos.to_tax_df(df, b_infos.format_tax_data)
    b_infos.export_by_depart_type(
        tax_res, period, departs.tax_departs(), filename='工资薪金所得', depart_type=utils.tax_column_name)
    b_infos.export_by_depart_type(
        tax_res, period, departs.depart_dispaly_names(), filename='工资薪金所得', depart_type=utils.depart_display_column_name)
