#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   test_salarys.py
@Time    :   2021/10/26 08:35:18
@Author  :   Tong tan 
@Version :   1.0
@Contact :   tongtan@gmail.com
'''


import src.salarys.period as period


class TestSalarys:

    def test_period(self):
        p = period.Period()
        p.get_period()
        assert p.df is not None
        assert p.year != 9999
        p.change_period(2021, 11)
        assert p.year == 2021
        assert p.month == 11
