#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   test_pandas.py
@Time    :   2021/03/12 14:23:58
@Author  :   Tong tan 
@Version :   1.0
@Contact :   tongtan@gmail.com
'''


import pytest

import numpy as np
import pandas as pd

import src.pandas.read_xls as prx


class TestPandas:

    filename = r'D:\薪酬审核文件夹\202103\汇总数据\202103_sh002.xls'

    path_prefix = r'D:\薪酬审核文件夹'
    period_str = '202110'
    salary_files_folder_path_name = '工资奖金数据'
    gz_file_name_prefix = '工资信息'
    jj_file_name_prefix = '奖金信息'

    def test_series(self):
        s = pd.Series([1, 3, 5, np.nan, 6, 8], name="something")
        assert s.max() == 8
        assert s[0] == 1
        assert pd.isna(s[3])
        assert 1 in s
        with pytest.raises(KeyError):
            s["f"]
        assert s.name == "something"

        s_1 = pd.Series(data=[100, 200, 300], index=['a', 'b', 'c'])
        assert s_1.index[0] == 'a'
        assert s_1.dtype == 'int64'
        assert s_1['a'] == 100
        assert 'a' in s_1

        s_2 = pd.Series(data=[100, 200, 300, 400], index=[1, 3, 5, 7])
        assert 1 in s_2
        assert s_2[1] == 100
        with pytest.raises(KeyError):
            s_2.loc[2]
        assert s_2.iloc[1] == 200
        assert s_2.iloc[2] == 300

    def test_dataframe(self):
        df = pd.DataFrame(
            {
                "Name": ["liqin", "wangting", "tongtan", "guowen"],
                "ChineseName": ["李琴", "王婷", "童坦", "郭雯"]
            }
        )
        df["OldName"] = df["Name"]
        assert df[df['ChineseName'] ==
                  '童坦']['Name'].values[0] == 'tongtan'
        assert "liqin" == df["Name"][0]
        assert "liqin" == df["OldName"][0]
        assert len(df.columns) == 3
        assert len(df[0:2]) == 2

    def test_read_excel(self):
        df = pd.read_excel(self.filename, sheet_name='Sheet1')
        assert df.loc[0, "员工姓名"] == '姜益民'
        assert df.iloc[0, 7] == '姜益民'

        assert len(df.columns) > 0
        assert df.columns[0] == '实发核对'
        assert df["实发核对"].sum() == 0

        code_grp = df.set_index("员工编号")
        s = code_grp.sum()

        assert s.loc["实发核对"] == 0
        assert s.loc["岗位工资"] == 31768087
        assert s.loc["保留工资"] == 3346804.5
        assert s.iloc[8] == 3346804.5

        avg = code_grp.mean()

        assert round(avg.loc["岗位工资"], 2) == 1723.44

        dw_grp = df.groupby("二级组织")
        assert len(dw_grp) == 13

        dw_grp_sum = dw_grp.sum()
        assert dw_grp_sum.loc["保卫部（武装部）", "岗位工资"] == 1283880
        assert dw_grp_sum.loc["教培中心", "保留工资"] == 62672

    def test_merge_excel_file_to_df(self):
        '''
        测试从单个excel文件合并数据
        '''
        df = prx.make_df_from_excel_files('202111')

        assert '工资信息-员工通行证' in df.columns
        assert '工资信息-应发' in df.columns

    def test_file_name_prefix_valitor(self):
        assert prx.file_name_prefix_validator("工资信息-股份.xlsx", "工资信息") is True
        assert prx.file_name_prefix_validator("~工资信息-股份.xlsx", "工资信息") is False

    def test_make_df_from_excel_files(self):
        # df_jj = prx.make_df_from_excel_files('202111', file_name_prefix='奖金信息', group_by=[
        #                                      '员工通行证', '员工姓名', '机构'])
        # df_jj = df_jj.loc[df_jj['奖金信息-员工通行证'] == 'M70359']
        # assert df_jj['奖金信息-员工通行证'] == 'M73677'
        df_gz = prx.make_df_from_excel_files('202111', file_name_prefix='工资信息')
        df_gz = df_gz.loc[df_gz['工资信息-员工通行证'] == 'M70359']
        type_str = type(df_gz)
        assert df_gz['工资信息-员工通行证'].values[0] == 'M70359'

    def test_df_merge(self):
        df_jj = prx.make_df_from_excel_files('202111', file_name_prefix='奖金信息', group_by=[
                                             '员工通行证', '员工姓名', '机构'])
        df_gz = prx.make_df_from_excel_files('202111', file_name_prefix='工资信息')

        df = pd.merge(df_gz, df_jj, left_on=[
                      '工资信息-员工通行证', '工资信息-机构'], right_on=['奖金信息-员工通行证', '奖金信息-机构'], how='outer')
        df_1 = df.loc[(df['工资信息-员工通行证'] == 'M70359') & (df['工资信息-机构']
                                                        == r'马钢（集团）控股有限公司(总部)\资产经营公司\综合管理部')]
        assert df_1['工资信息-员工通行证'].values[0] == 'M70359'
        assert df_1['奖金信息-员工通行证'].values[0] == 'M70359'
        assert df_1['奖金信息-应发'].values[0] > 0
        df_2 = df.loc[(df['奖金信息-员工通行证'] == 'M73677') & (df['奖金信息-机构']
                                                        == r'马钢（集团）控股有限公司(总部)\资产经营公司\工程管理部')]
        assert df_2['奖金信息-员工通行证'].values[0] == 'M73677'
        assert df_2['奖金信息-应发'].values[0] == 12900
