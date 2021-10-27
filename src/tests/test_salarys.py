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
        assert gzs.df[f'{gzs.name}-员工通行证'].any()

        jjs = s_infos.SalaryJjs(period, departs=ds)
        assert ~jjs.df.empty
        assert jjs.df[f'{jjs.name}-员工通行证'].any()

        banks = s_infos.SalaryBanks(period, departs=ds)
        assert ~gzs.df.empty
        assert banks.df[f'{banks.name}-员工通行证'].any()

        jobs = s_infos.SalaryPersonJobs(period, departs=ds)
        assert ~jobs.df.empty
        assert jobs.df[f'{jobs.name}-员工通行证'].any()

        persons = s_infos.SalaryPersons(period)
        assert ~persons.df.empty
        assert persons.df[f'{persons.name}-员工通行证'].any()

    # def test_salary_infos_taxs(self):
    #     ds = depart_op.Departs(period=period)
    #     taxs = s_infos.SalaryTaxs(period, ds.tax_departs())
    #     assert len(taxs) == 2

    def test_depart_display_info(self):
        ds = depart_op.Departs(period=period)
        gzs = s_infos.SalaryGzs(period, ds)
        assert ~gzs.df.empty
        assert gzs.df[f'{gzs.name}-员工通行证'].any()
        assert gzs.df[f'{gzs.name}-{utils.depart_display_column_name}'].any()
