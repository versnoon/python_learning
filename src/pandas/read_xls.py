import pytest

import os
import numpy as np
import pandas as pd


# 存放数据文件的根目录
file_root_path = r'D:\薪酬审核文件夹'

# 一次读取多少条记录
rows_per_one_read = 3000


def make_df_from_excel_files(
    period='',
    file_sub_path='工资奖金数据',
    file_name_prefix='工资信息',
    file_exts=['.xls', '.xlsx'],
    group_by=[]
):
    chunks = []
    file_dir = get_file_dir(period, file_sub_path)
    for file_name in os.listdir(file_dir):
        if file_name_validate(file_name, file_name_prefix, file_exts):
            file_df = make_df_from_excel(get_file_path(
                file_dir, file_name), file_name_prefix)
            chunks.append(file_df)
    if len(chunks) > 0:
        df = pd.concat(chunks, ignore_index=True)
    if len(group_by) > 0:
        group_by_keys = [f'{file_name_prefix}-{col}' for col in group_by]
        df = df.groupby(group_by_keys, as_index=False)
        df = df.aggregate(np.sum)
    return df


def get_file_dir(period='', file_sub_path=''):
    p = file_root_path
    if period:
        p = os.path.join(p, period)
    if file_sub_path:
        p = os.path.join(p, file_sub_path)
    return p


def get_file_path(dir, file_name):
    return os.path.join(dir, file_name)


def file_name_validate(file_name, file_name_prefix, file_exts):
    return file_name_prefix_validator(file_name, file_name_prefix) and file_ext_validator(file_name, file_exts)


def file_name_prefix_validator(file_name, file_name_prefix):
    return file_name.startswith(file_name_prefix)


def file_ext_validator(file_name, file_exts):
    file_ext = get_file_ext(file_name)
    if file_ext in file_exts:
        return True
    return False


def make_df_from_excel(file_path, name):
    head_row = 1
    df_header = pd.read_excel(file_path, nrows=head_row)
    # Rename the columns to concatenate the chunks with the header.
    columns = {i: f'{name}-{col}' for i,
               col in enumerate(df_header.columns.tolist())}

    df_chunks = pd.read_excel(file_path, skiprows=head_row, header=None)

    df_chunks.rename(columns=columns, inplace=True)
    return df_chunks


def get_file_ext(file_path):
    """
    获取文件的后缀并统一抓换为小写
    """
    ext = os.path.splitext(file_path)
    if len(ext) == 0:
        return ""
    return ext[-1].lower()


def get_df_cell_value(df, perfix, name, row=0):
    key = name
    if perfix:
        key = f'{perfix}-{name}'
    return df[key].values[row]
