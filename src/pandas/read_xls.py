import pytest

import os
import numpy as np
import pandas as pd


# 存放数据文件的根目录
file_root_path = r'D:\薪酬审核文件夹'
# 期间信息
period = '202110'

sub_path = '工资奖金数据'


def test_pd():
    pd.Series([1, 3, 5, np.nan, 6, 8])


def make_df_from_excel(filename, skiperror=True):
    file_path = get_file_path(filename)
    if os.path.exists(file_path):
        pass
    else:
        if not skiperror:
            raise FileNotFoundError(f"无法读取{file_path}文件")
    return file_path


def get_file_dir():
    """
    获取需要读取文件的存放目录
    """
    return os.path.join(file_root_path, period, sub_path)


def get_file_path(filename):
    return os.path.join(get_file_dir(), filename)
