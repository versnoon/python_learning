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
import src.pandas.read_xls as prx
import src.salarys.salary_infos as s_infos


class TestSalarys:

    def test_period(self):
        p = period_op.Period()
        assert p.df is not None
        assert p.year != 9999
        p.change_period(2021, 11)
        assert p.year == 2021
        assert p.month == 11

    def test_departs(self):
        ds = depart_op.Departs(period='202111')
        assert ds.df is not None
        assert len(ds.departs) > 0
        assert ds.departs[0].name == '集团机关'
        assert len(ds.departs[0].children_names) > 0
        assert f'马钢（集团）控股有限公司(总部){utils.depart_sep}办公室（党委办公室）' in ds.departs[
            0].children_names
        assert ds.departs[0].display_name == '集团机关'

    def test_salary_infos(self):
        gzs = s_infos.SalaryGzs('202111')
        assert gzs.df is not None
        assert gzs.df[f'{gzs.name}-员工通行证'].any()

        jjs = s_infos.SalaryJjs('202111')
        assert ~jjs.df.empty
        assert jjs.df[f'{jjs.name}-员工通行证'].any()

        banks = s_infos.SalaryBanks('202111',)
        assert banks.df.empty
