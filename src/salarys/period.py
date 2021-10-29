#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   period.py
@Time    :   2021/10/25 17:13:54
@Author  :   Tong tan 
@Version :   1.0
@Contact :   tongtan@gmail.com
'''


from os import error
from numpy import e
import src.salarys.utils as utils
import src.salarys.data_read as prx


class Period:
    """
    处理期间相关数据
    """

    def __init__(self) -> None:
        self.year = 9999
        self.month = 12
        self.name = '当前审核日期'
        self.df = None
        self.get_period()
        self.err_paths = []

    def get_period(self):
        if not self.df:
            self.df, self.err_paths = prx.make_df_from_excel_files(
                file_root_path=utils.root_dir_(), file_name_prefix=self.name)
        if not self.df.empty:
            self.year = prx.get_df_cell_value(self.df, '年')
            self.month = prx.get_df_cell_value(self.df, '月')
        else:
            err_file_msg = '|'.join(self.err_paths)
            raise ValueError(f'获取期间数据出错，错误文件:[{err_file_msg}]数据内容为空，或者文件不存在')

    def change_period(self, year, month):
        self.year = year
        self.month = month

    def get_period_info(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return "{:0>4d}{:0>2d}".format(int(self.year), int(self.month))
