#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   depart.py
@Time    :   2021/10/26 09:00:29
@Author  :   Tong tan 
@Version :   1.0
@Contact :   tongtan@gmail.com
'''


import pandas as pd
import src.salarys.utils as utils
import src.salarys.data_read as prx


class Depart:

    def __init__(self) -> None:
        self.name = ''  # 机构名称
        self.display_name = ''  # 机构显示名称
        self.children_names = []  # 相关单位
        self.scope_no = ''  # 薪酬范围
        self.sort_no = 99  # 显示顺序
        self.tax_dep_name = ''  # 税务机构
        self.gjj_dep_name = ''  # 公积金类别
        self.his_names = []  # 历史机构名称
        self.sep = '|'  # 默认机构间分隔符


class Departs:

    def __init__(self, period=None) -> None:
        self.departs = []
        self.period = period
        self.df = None
        self.name = '审核机构信息'
        self.get_departs()
        self.err_paths = []

    def get_departs(self):
        if not self.period:
            raise ValueError(f'请指定期间信息')
        if not self.df:
            self.df, self.err_paths = prx.make_df_from_excel_files(
                period=self.period, file_root_path=utils.root_dir_(), file_name_prefix=self.name)
        if not self.df.empty:
            self.departs = self.to_depart_infos(self.df)

    def to_depart_infos(self, df: pd.DataFrame) -> list:
        return list(map(lambda s: self.to_depart_info(s), df.values.tolist()))

    def to_depart_info(self, s) -> Depart:
        d = Depart()
        d.sort_no = s[0]
        d.scope_no = s[1]  # 工资范围
        d.display_name = s[2]  # 机构显示名称
        d.name = s[3]  # ehr系统中单位名称
        d.tax_dep_name = s[6]  # 税务机构
        if s[4]:
            if isinstance(s[4], str):
                d.children_names = list(map(
                    lambda x: f'{d.tax_dep_name}{utils.depart_sep}{x}', s[4].split(d.sep)))  # 相关单位
        if s[4]:
            if isinstance(s[8], str):
                d.his_names = list(map(
                    lambda x: f'{d.tax_dep_name}{utils.depart_sep}{x}', s[8].split(d.sep)))  # 相关单位
        d.gjj_dep_name = s[7]  # 公积金类型
        return d

    def tax_departs(self):
        return self.df[f"{self.name}-税务机构"].drop_duplicates().to_list()
