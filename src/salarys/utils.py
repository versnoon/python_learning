#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   utils.py
@Time    :   2021/10/25 17:14:58
@Author  :   Tong tan 
@Version :   1.0
@Contact :   tongtan@gmail.com
'''

import os
import shutil


# 文件跟目录
root_dir = r'D:\薪酬审核文件夹'
test_dir = 'test'
gz_jj_dir = '工资奖金数据'
gz_file_prefix = '工资信息'
jj_file_prefix = '奖金信息'
tax_dir = '税务相关数据'
insurance_dir = '三险两金数据'
result_dir = '审核结果数据'
depart_file_name = '审核机构信息.xls'
period_file_name = '当前审核日期'

depart_sep = '-X-'
column_name_sep = '-'
column_name_suffix_sep = '_'
depart_info_sep = '\\'


depart_info_column_name = '机构'
code_info_column_name = '员工通行证'
name_info_column_name = '员工姓名'

tax_column_name = '税务机构'
depart_column_name = '单位名称'
depart_display_column_name = '单位显示名称'
person_id_column_name = '证件号码'

yingfa_column_name = '应发合计'
shifa_column_name = '实发合计'
shouru_column_name = '本期收入'
suodeshui_column_name = '所得税'
suodeshui_column_name_o = '所得税_o'
jigou_column_name = '机构全路径'

gjj_v_column_name = '公积金验证'

max_gjj = 2679  # 公积金上限
max_nj = 894  # 年金上限

err_folder_name = '审核错误信息'
tax_folder_name = '税务系统_工资薪金所得'
pdf_folder_name = '拨款单'
person_compare_folder_name = '人员上下月对比'
sap_folder_name = 'sap格式数据'


def root_dir_() -> str:
    path = os.path.join(root_dir)
    return path


def join_path(paths) -> str:
    path = root_dir_()
    for p in paths:
        path = os.path.join(path, p)
    return path


def file_path_exists(path, filename) -> bool:
    path = os.path.join(path, filename)
    if os.path.exists(path) and os.path.isfile(path):
        return True, path
    return False, path


def file_path(path, filename) -> str:
    if not os.path.exists(path):
        os.makedirs(path)
    return os.path.join(path, filename)


def clear_folder_by_paths(path):
    if os.path.exists(path):
        shutil.rmtree(path)


def make_folder_if_nessage(path) -> str:
    if not os.path.exists(path):
        os.makedirs(path)


def copy_file(file_path, dst_file):
    shutil.copyfile(file_path, dst_file)
