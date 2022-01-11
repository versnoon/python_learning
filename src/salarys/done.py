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


def audit():
    # 加载数据
    p, departs, persons, gzs, jjs, banks, tax, taxOne, gjjs = b_infos.load_data()
    df = b_infos.contact_info(
        gzs, jjs, banks=banks, persons=persons, tax=tax, taxOne=taxOne, gjjs=gjjs, departs=departs)
    period = p.get_period_info()
    errs = b_infos.validator(df)
    if len(errs) > 0:
        # 输出汇总信息
        s_infos.export_all_errs(period, errs)
        # 根据税务单位输出数据
        s_infos.export_errs_by_depart_type(
            period, errs, departs.tax_departs(), utils.tax_column_name)
        #  根据显示单位输出数据
        s_infos.export_errs_by_depart_type(
            period, errs, departs.depart_dispaly_names())
    else:
        # sap_df = s_infos.to_sap_frame(df)
        tax_res = b_infos.to_tax_df(df, b_infos.format_tax_data)
        b_infos.export_by_depart_type(
            tax_res, period, departs.tax_departs(), filename='工资薪金所得', depart_type=utils.tax_column_name)
        b_infos.export_by_depart_type(
            tax_res, period, departs.depart_dispaly_names(), filename='工资薪金所得', depart_type=utils.depart_display_column_name)
        if s_infos.get_column_name(s_infos.SalaryJjs.name, '年底兑现奖') in df.columns:
            tax_res = b_infos.to_tax_df_one(df)
            b_infos.export_by_depart_type(
                tax_res, period, departs.tax_departs(), filename='全年一次性奖金收入', depart_type=utils.tax_column_name)
            b_infos.export_by_depart_type(
                tax_res, period, departs.depart_dispaly_names(), filename='全年一次性奖金收入', depart_type=utils.depart_display_column_name)


def compare_person():
    # 导出根据上下月发工资名单的不同计算人员变化情况并导出
    current_p = b_infos.load_period()

    c_period = current_p.get_period_info()
    p_period = current_p.get_pre_period_info()
    c_gz = b_infos.load_gz_by_period(c_period)
    c_persons = b_infos.load_person_info(c_period)
    c = b_infos.contact_id_info(c_gz.df, c_persons)
    p_gz = b_infos.load_gz_by_period(p_period)
    p_persons = b_infos.load_person_info(p_period)
    p = b_infos.contact_id_info(p_gz.df, p_persons)
    departs = b_infos.load_depart(c_period)
    # 增加的人

    # 分单位导出
    b_infos.person_compare(
        c_period, c, p, departs.depart_dispaly_names())
    # 分税务单位导出
    b_infos.person_compare(
        c_period, c, p, departs.tax_departs(), depart_type=utils.tax_column_name)

    # 人力资源服务中心
    b_infos.person_compare(
        c_period, c, p, ['人力资源服务中心1'], depart_type=utils.depart_column_name)


def to_salary_pdf():
    p, departs, persons, gzs, jjs, banks, tax, taxOne, gjjs = b_infos.load_data()
    df = b_infos.contact_info(
        gzs=gzs, jjs=jjs, banks=banks, persons=persons, tax=tax, taxOne=taxOne, gjjs=gjjs, departs=departs)
    b_infos.to_salary_pay(p.get_period_info(), departs, df)
