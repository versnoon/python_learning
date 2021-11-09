#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   test_salarys.py
@Time    :   2021/10/26 08:35:18
@Author  :   Tong tan 
@Version :   1.0
@Contact :   tongtan@gmail.com
'''


import src.salarys.period as period_op
import src.salarys.depart as depart_op
import src.salarys.utils as utils
import src.salarys.salary_infos as s_infos

period = '202110'


class TestSalarys:

    def test_period(self):
        p = period_op.Period()
        assert p.df is not None
        assert p.year != 9999
        p.change_period(2021, 11)
        assert p.year == 2021
        assert p.month == 11

    def test_departs(self):
        ds = depart_op.Departs(period=period)
        assert ds.df is not None
        assert len(ds.departs) > 0
        assert ds.departs[0].name == '集团机关'
        assert len(ds.departs[0].children_names) > 0
        assert f'马钢（集团）控股有限公司(总部){utils.depart_sep}办公室（党委办公室）' in ds.departs[
            0].children_names
        assert f'马钢（集团）控股有限公司(总部){utils.depart_sep}人力资源服务中心' in ds.departs[
            0].his_names
        assert ds.departs[0].display_name == '集团机关'
        assert "集团机关" == ds.display_depart_name(
            "马钢（集团）控股有限公司(总部)", "办公室（党委办公室）")
        assert "集团机关" == ds.display_depart_name(
            "马钢（集团）控股有限公司(总部)", "人力资源服务中心")
        assert "" == ds.display_depart_name(
            "马钢（集团）控股有限公司(总部)", "办公室（党委办公室）1")

    def test_salary_infos(self):
        ds = depart_op.Departs(period=period)
        gzs = s_infos.SalaryGzs(period, departs=ds)
        assert ~gzs.df.empty
        assert gzs.df[f'员工通行证'].any()

        jjs = s_infos.SalaryJjs(period, departs=ds)
        assert ~jjs.df.empty
        assert jjs.df[f'员工通行证'].any()

        banks = s_infos.SalaryBanks(period, departs=ds)
        assert ~banks.df.empty
        assert banks.df[f'员工通行证'].any()

        jobs = s_infos.SalaryPersonJobs(period, departs=ds)
        assert ~jobs.df.empty
        assert jobs.df[f'员工通行证'].any()

        persons = s_infos.SalaryPersons(period)
        assert ~persons.df.empty
        assert persons.df[f'员工通行证'].any()

    def test_salary_infos_taxs(self):
        ds = depart_op.Departs(period=period)
        taxs = s_infos.SalaryTaxs(period, ds.tax_departs())
        assert ~taxs.df.empty
        assert taxs.df['证件号码'].any()
        assert taxs.df[utils.tax_column_name].any()

    def test_depart_display_info(self):
        ds = depart_op.Departs(period=period)
        gzs = s_infos.SalaryGzs(period, ds)
        assert ~gzs.df.empty
        assert gzs.df[f'员工通行证'].any()
        assert gzs.df[utils.depart_display_column_name].any()

    def test_bank_info(self):
        ds = depart_op.Departs(period=period)
        banks = s_infos.SalaryBanks(period, departs=ds)
        assert ~banks.df.empty
        assert banks.df[f'员工通行证'].any()
        gz = s_infos.get_value_with_suffix(
            banks.df, banks.name, "M08175", "卡号", '工资卡')
        assert gz == 1306212001001966586
        assert s_infos.get_value_with_suffix(
            banks.df, banks.name, "M08175", "卡号", '奖金卡') == 1306212001001966586
        assert s_infos.get_value_with_suffix(
            banks.df, banks.name, "M70847", "卡号", '奖金卡') == 6212261306001042571

    def test_contact_some_info(self):
        ds = depart_op.Departs(period=period)
        gzs = s_infos.SalaryGzs(period, departs=ds)
        assert ~gzs.df.empty
        jjs = s_infos.SalaryJjs(period, departs=ds)
        persons = s_infos.SalaryPersons(period)
        s = s_infos.merge_gz_and_jj(gzs, jjs)
        s.to_excel('s.xlsx')
        assert s_infos.get_value(
            s, "", "M73677", "应发合计") == 3712.6 + 17561
        assert s_infos.get_value(
            s, "", "M73677", "实发合计") == 155.78 + 16589.32
        assert s_infos.get_value(
            s, "", "M73677", "所得税") == 0 - (0 + -971.68)
        s = s_infos.contact_id_info(s, persons)
        assert s_infos.get_value(
            s, "", "M73677", utils.code_info_column_name) == "M73677"
        assert s[f'{persons.name}-{utils.person_id_column_name}'].any()
        assert s_infos.get_value(s, "", "M73677", s_infos.get_column_name(
            persons.name, utils.person_id_column_name)) == '34022219820226691X'
        banks = s_infos.SalaryBanks(period, departs=ds)
        s = s_infos.contact_bank_info(s, banks)
        assert s[f'{banks.name}-卡号_工资卡'].any()
        assert s[f'{banks.name}-卡号_奖金卡'].any()
        assert s_infos.get_value_with_suffix(
            s, banks.name, "M73677", "卡号", "工资卡") == '6217231306000241097'
        assert s_infos.get_value_with_suffix(
            s, banks.name, "M73677", "卡号", "奖金卡") == '6217231306000241097'
        jobs = s_infos.SalaryPersonJobs(period, departs=ds)
        s = s_infos.contact_job_info(s, jobs)
        assert s[f'{jobs.name}-岗位类型'].any()
        assert s_infos.get_value(s, "", "M73677", s_infos.get_column_name(
            jobs.name, "岗位类型")) == '管理类'
        taxs = s_infos.SalaryTaxs(period, ds.tax_departs())
        s = s_infos.contact_tax_info(s, taxs)
        assert s["累计应补(退)税额"].any()
        assert s_infos.get_value(s, "", "M73677", "累计应补(退)税额") == 971.68
