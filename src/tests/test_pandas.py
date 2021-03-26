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


class TestPandas:

    filename = r'D:\薪酬审核文件夹\202103\汇总数据\202103_sh002.xls'

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
