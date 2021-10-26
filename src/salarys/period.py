#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   period.py
@Time    :   2021/10/25 17:13:54
@Author  :   Tong tan 
@Version :   1.0
@Contact :   tongtan@gmail.com
'''


import src.salarys.utils as utils
import src.pandas.read_xls as prx


class Period:
    """
    处理期间相关数据
    """

    def __init__(self) -> None:
        self.year = 9999
        self.month = 12
        self.name = '当前审核日期'
        self.df = None

    def get_period(self):
        if not self.df:
            self.df = prx.make_df_from_excel_files(
                file_root_dir=utils.root_dir, file_name_prefix=self.name)
        self.year = prx.get_df_cell_value(self.df, '当前审核日期', '年')
        self.month = prx.get_df_cell_value(self.df, '当前审核日期', '月')

    def change_period(self, year, month):
        self.year = year
        self.month = month

    def __str__(self) -> str:
        return "{:0>4d}{:0>2d}".format(int(self.year), int(self.month))
