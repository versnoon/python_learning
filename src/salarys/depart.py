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
        self.display_names = self.display_depart_names()
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
        if s[8]:
            if isinstance(s[8], str):
                d.his_names = list(map(
                    lambda x: f'{d.tax_dep_name}{utils.depart_sep}{x}', s[8].split(d.sep)))  # 历史
        d.gjj_dep_name = s[7]  # 公积金类型
        return d

    def tax_departs(self):
        return self.df["税务机构"].drop_duplicates().to_list()

    def depart_dispaly_names(self):
        return self.df["SAP单位名称"].drop_duplicates().to_list()

    def display_depart_name(self, tax, depart_name):
        key = f"{tax}{utils.depart_sep}{depart_name}"
        if key in self.display_names:
            return self.display_names[key]
        return ""

    def is_in_tax_depart(self, tax, depart):
        for k, v in self.display_names.items():
            if k.startswith(tax) and v == depart:
                return True
        return False

    def display_depart_names(self):
        r = dict()
        for d in self.departs:
            tax = d.tax_dep_name
            depart_name = d.name
            display_name = d.display_name
            children_names = d.children_names
            his_names = d.his_names
            r[f"{tax}{utils.depart_sep}{depart_name}"] = display_name
            for c_name in children_names:
                r[f"{c_name}"] = display_name
            for h_name in his_names:
                r[f"{h_name}"] = display_name
        return r

    def get_bw__gjj_fangan(self, tax_depart, gjj_type, display_depart):
        if not pd.isna(gjj_type):
            departs_list = self.df[self.df["公积金中心"] ==
                                   gjj_type]['SAP单位名称'].drop_duplicates().to_list()
            if tax_depart == '马鞍山钢铁股份有限公司（总部）':
                if not display_depart in departs_list:
                    return 'ERR'
        return 'OK'

    def get_gjj_fangan(self, tax_depart, gjj_type, display_depart):
        if not pd.isna(gjj_type):
            departs_list = self.df[self.df["公积金中心"] ==
                                   gjj_type]['SAP单位名称'].drop_duplicates().to_list()
            if tax_depart == '马鞍山钢铁股份有限公司（总部）':
                if not display_depart in departs_list:
                    return 'ERR'
        return 'OK'
