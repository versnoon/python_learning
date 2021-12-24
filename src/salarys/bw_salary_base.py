#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   bw_salary_base.py
@Time    :   2021/12/24 09:28:34
@Author  :   Tong tan 
@Version :   1.0
@Contact :   tongtan@gmail.com
'''

import src.salarys.errs as errs


class BaseInfo:

    def __init__(self, name='') -> None:
        self.name = name


class PeriodBaseInfo(BaseInfo):
    def __init__(self, name='', period=None) -> None:
        if not period:
            raise errs.NOT_FOUND_PERIOD_ERR
        super().__init__(name=name)
        self.period = period
