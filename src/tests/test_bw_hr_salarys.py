#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   test_bw_hr_salarys.py
@Time    :   2021/11/24 16:09:05
@Author  :   Tong tan 
@Version :   1.0
@Contact :   tongtan@gmail.com
'''

from src.salarys import bw_hr_salary, pdf_gen
from src.salarys import salary_infos
from src.salarys import utils
from src.salarys import bw_salary_modes


class TestBwSalarys:

    def test_init_bw_folder(self):
        bw_hr_salary.init()
        p, departs, persons, gzs, jjs, banks, tax, taxOne, gjjs = bw_hr_salary.load_data()
        df = bw_hr_salary.contact_info(
            gzs, jjs, banks=banks, persons=persons, tax=tax, taxOne=taxOne, gjjs=gjjs, departs=departs)
        period = p.get_period_info()
        errs = bw_hr_salary.validator(df)
        if len(errs) > 0:

            # 输出汇总信息
            salary_infos.export_all_errs(period, errs)
        # 根据税务单位输出数据
            salary_infos.export_errs_by_depart_type(
                period, errs, departs.tax_departs(), utils.tax_column_name)
        #  根据显示单位输出数据
            salary_infos.export_errs_by_depart_type(
                period, errs, departs.depart_dispaly_names())
        sap = salary_infos.to_sap_frame(df)
        sap.to_excel(f'{period}_sh002.xlsx')
        # else:
        #     # 输出相关表格
        #     # 数据税表
        #     pass

    def test_tax_export(self):
        bw_hr_salary.init()
        _, departs, persons, gzs, jjs, banks, tax, taxOne, gjjs = bw_hr_salary.load_data()
        df = bw_hr_salary.contact_info(
            gzs, jjs, banks=banks, persons=persons, tax=tax, taxOne=taxOne, gjjs=gjjs, departs=departs)
        tax_res = bw_hr_salary.to_tax_df(df, bw_hr_salary.format_tax_data_o)
        tax_res.to_excel('tax.xlsx', sheet_name='工资薪金所得')

    def test_new_bw_salary_ops(self):
        bw_salary_modes.load_period_info()
        assert bw_salary_modes.period_info['year'] == 2021
        assert bw_salary_modes.period_info['month'] == 12
        assert bw_salary_modes.period() == '202112'
        assert bw_salary_modes.pre_period() == '202111'

    def test_tax_export_one(self):
        bw_hr_salary.init()
        _, departs, persons, gzs, jjs, banks, tax, taxOne, gjjs = bw_hr_salary.load_data()
        df = bw_hr_salary.contact_info(
            gzs, jjs, banks=banks, persons=persons, tax=tax, taxOne=taxOne, gjjs=gjjs, departs=departs)
        if salary_infos.get_column_name(salary_infos.SalaryJjs.name, '年底兑现奖') in df.columns:
            tax_res = bw_hr_salary.to_tax_df_one(df)
            tax_res.to_excel('tax_one.xlsx', sheet_name='全年一次性奖金收入')

    def test_export_split_2(self):
        bw_hr_salary.init()
        p, departs, persons, gzs, jjs, banks, tax, taxOne, gjjs = bw_hr_salary.load_data()
        df = bw_hr_salary.contact_info(
            gzs=gzs, jjs=jjs, banks=banks, persons=persons, tax=tax, taxOne=taxOne, gjjs=gjjs, departs=departs)
        period = p.get_period_info()
        tax_res = bw_hr_salary.to_tax_df(df, bw_hr_salary.format_tax_data_o)
        bw_hr_salary.export_by_depart_type(
            tax_res, period, departs.tax_departs(), filename='工资薪金所得', depart_type=utils.tax_column_name)
        bw_hr_salary.export_by_depart_type(
            tax_res, period, departs.depart_dispaly_names(), filename='工资薪金所得', depart_type=utils.depart_display_column_name)

    def test_export_split(self):
        bw_hr_salary.init()
        p, departs, persons, gzs, jjs, banks, tax, taxOne, gjjs = bw_hr_salary.load_data()
        df = bw_hr_salary.contact_info(
            gzs=gzs, jjs=jjs, banks=banks, persons=persons, tax=tax, taxOne=taxOne, gjjs=gjjs, departs=departs)
        period = p.get_period_info()
        if salary_infos.get_column_name(salary_infos.SalaryJjs.name, '年底兑现奖') in df.columns:
            tax_res = bw_hr_salary.to_tax_df_one(df)
            bw_hr_salary.export_by_depart_type(
                tax_res, period, departs.tax_departs(), filename='全年一次性奖金收入', depart_type=utils.tax_column_name)
            bw_hr_salary.export_by_depart_type(
                tax_res, period, departs.depart_dispaly_names(), filename='全年一次性奖金收入', depart_type=utils.depart_display_column_name)

    def test_pdf_export_one(self):
        p, departs, persons, gzs, jjs, banks, tax, taxOne, gjjs = bw_hr_salary.load_data()
        df = bw_hr_salary.contact_info(
            gzs=gzs, jjs=jjs, banks=banks, persons=persons, tax=tax, taxOne=taxOne, gjjs=gjjs, departs=departs)
        bw_hr_salary.to_salary_pay(p.get_period_info(), departs, df)

    def test_person_compare(self):
        current_p = bw_hr_salary.load_period()

        c_period = current_p.get_period_info()
        p_period = current_p.get_pre_period_info()
        c_gz = bw_hr_salary.load_gz_by_period(c_period)
        c_persons = bw_hr_salary.load_person_info(c_period)
        c = bw_hr_salary.contact_id_info(c_gz.df, c_persons)
        p_gz = bw_hr_salary.load_gz_by_period(p_period)
        p_persons = bw_hr_salary.load_person_info(p_period)
        p = bw_hr_salary.contact_id_info(p_gz.df, p_persons)
        departs = bw_hr_salary.load_depart(c_period)
        # 增加的人

        # 分单位导出
        bw_hr_salary.person_compare(
            c_period, c_gz.df, p_gz.df, departs.depart_dispaly_names())
        # 分税务单位导出
        bw_hr_salary.person_compare(
            c_period, c, p, departs.tax_departs(), depart_type=utils.tax_column_name)

    def test_person_merge(self):
        current_p = bw_hr_salary.load_period()
        c_persons = bw_hr_salary.load_person_info(current_p.get_period_info())
        df = c_persons.df
        assert not df.empty
        assert not df[df[utils.code_info_column_name] == 'M99999'].empty
