#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   bw_salary_modes.py
@Time    :   2021/12/24 09:39:30
@Author  :   Tong tan 
@Version :   1.0
@Contact :   tongtan@gmail.com
'''

import src.salarys.bw_salary_base as bw_salary_base


class Period(bw_salary_base.BaseInfo):

    model_name = '期间信息'

    def __init__(self) -> None:
        super().__init__(name=self.model_name)
