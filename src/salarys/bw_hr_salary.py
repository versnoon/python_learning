#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   bw_hr_salary.py
@Time    :   2021/11/24 15:44:01
@Author  :   Tong tan
@Version :   1.0
@Contact :   tongtan@gmail.com
'''
import os
import shutil
import pandas as pd
from src.salarys import utils

from src.salarys.utils import join_path, file_path_exists, make_folder_if_nessage, copy_file, gz_jj_dir, tax_dir, insurance_dir, result_dir, depart_file_name, gz_file_prefix, jj_file_prefix, code_info_column_name, person_id_column_name, tax_column_name, depart_display_column_name, name_info_column_name, yingfa_column_name, depart_column_name, file_path, shouru_column_name
from src.salarys.period import Period
from src.salarys.depart import Departs
from src.salarys.salary_infos import SalaryBanks, SalaryBaseInfo, SalaryGzs, SalaryJjs, SalaryTaxs, SalaryGjj, SalaryOneTaxs, get_column_name, merge_gz_and_jj, contact_bank_info, contact_tax_info, validator_bank_info, validator_sf_info, validator_id_info, validator_gjj, validator_other, validator_tax_info, get_export_path, contact_tax_validate, contact_tax_one_info
from src.salarys import pdf_gen


def format_tax_data(x):
    # 2020年公积金上限2680
    # 2020年年金894
    total, yl, yil, shiy, nj, gjj = 0, 0, 0, 0, 0, 0
    if not x.empty:
        total = x['本期收入']
        if pd.isna(total):
            total = 0
        yl = x['基本养老保险费']
        if not pd.isna(yl):
            if yl < 0:
                total = total - yl
                yl = 0
            else:
                yl = abs(yl)
        yil = x['基本医疗保险费']
        if not pd.isna(yil):
            if yil < 0:
                total = total - yil
                yil = 0
            else:
                yil = abs(yil)
        shiy = x['失业保险费']
        if not pd.isna(shiy):
            if shiy < 0:
                total = total - shiy
                shiy = 0
            else:
                shiy = abs(shiy)
        nj = x['企业(职业)年金']
        if not pd.isna(nj):
            if nj > utils.max_nj:
                total = total + (nj - utils.max_nj)
                nj = utils.max_nj
            else:
                nj = abs(nj)
        gjj = x['住房公积金']
        if not pd.isna(gjj):
            if gjj > (utils.max_gjj):
                total = total + (gjj - utils.max_gjj)
                gjj = utils.max_gjj
            else:
                gjj = abs(gjj)
    return round(total, 2), round(yl, 2), round(yil, 2), round(shiy, 2), round(gjj, 2), round(nj, 2)


def format_tax_data_o(x):
    # 2020年公积金上限2680
    # 2020年年金894
    total, yl, yil, shiy, nj, gjj = 0, 0, 0, 0, 0, 0
    if not x.empty:
        total = x['本期收入']
        if pd.isna(total):
            total = 0
        yl = x['基本养老保险费']
        if not pd.isna(yl):
            if yl > 0:
                total = total + yl
                yl = 0
            else:
                yl = abs(yl)
        yil = x['基本医疗保险费']
        if not pd.isna(yil):
            if yil > 0:
                total = total + yil
                yil = 0
            else:
                yil = abs(yil)
        shiy = x['失业保险费']
        if not pd.isna(shiy):
            if shiy > 0:
                total = total + shiy
                shiy = 0
            else:
                shiy = abs(shiy)
        nj = x['企业(职业)年金']
        if not pd.isna(nj):
            if nj < (0-utils.max_nj):
                total = total + (0 - nj - utils.max_nj)
                nj = utils.max_nj
            else:
                nj = abs(nj)
        gjj = x['住房公积金']
        if not pd.isna(gjj):
            if gjj < (0 - utils.max_gjj):
                total = total + (0-gjj - utils.max_gjj)
                gjj = utils.max_gjj
            else:
                gjj = abs(gjj)
    return round(total, 2), round(yl, 2), round(yil, 2), round(shiy, 2), round(gjj, 2), round(nj, 2)

# '基本医疗保险费', '失业保险费', '住房公积金', '企业(职业)年金',


def init():
    """
    根据期间初始化目录结构
    """
    p = load_period()
    period = p.get_period_info()
    init_folder_if_not_exists(period=period, folder_name=gz_jj_dir)
    init_folder_if_not_exists(period=period, folder_name=tax_dir)
    init_folder_if_not_exists(period=period, folder_name=insurance_dir)
    init_folder_if_not_exists(period=period, folder_name=result_dir)
    copy_depart_file_if_not_exists(p)
    clear(p)
    # rename_to_standard(p)


def clear(period):
    dir = join_path([period.get_period_info(), result_dir])
    shutil.rmtree(dir)
    os.mkdir(dir)


def rename_to_standard(period: Period):
    # 工资奖金
    standard_file_name(period, gz_jj_dir)


def standard_file_name(period, foldername):
    dir = join_path([period.get_period_info()])
    if foldername:
        dir = join_path([period.get_period_info(), foldername])
    dir_files = os.listdir(dir)
    for file in dir_files:
        if file.lower().endswith('xls') or file.lower().endswith('xlsx'):
            file_path = join_path([dir, file])
            df = pd.read_excel(file_path, nrows=1)
            rename_and_copy_file(period, df, file_path)


def rename_and_copy_file(period, df, file_path):
    file_name, depart_info = get_file_name_info(df)
    dst_file_path = join_path(
        [period.get_period_info(), result_dir, f"{file_name}-{depart_info}.xlsx"])
    shutil.copyfile(file_path, dst_file_path)


def get_file_name_info(df):
    file_name = ""
    if is_gz(df.columns):
        file_name = gz_file_prefix
    elif is_jj(df.columns):
        file_name = jj_file_prefix
    depart_info = get_depart_info_from_departs(df)
    return file_name, depart_info


def get_depart_info_from_departs(df):
    depart_info = ""
    ds = df["所在机构"].str.split("\\")
    depart_info = ds.iloc[0][0]
    for d in ds.iloc[0]:
        if "总部" in d:
            depart_info = d
            break
    return depart_info


def is_gz(columns):
    return check_columnname_in_columns("养老保险个人额度", columns)


def is_jj(columns):
    return check_columnname_in_columns("基本奖金", columns)


def check_columnname_in_columns(column_name, columns):
    return column_name in columns


def init_folder_if_not_exists(period, folder_name):
    dir = join_path([period, folder_name])
    make_folder_if_nessage(dir)


def copy_depart_file_if_not_exists(p: Period):
    dir = join_path([p.get_period_info()])
    exists, dst_filepath = file_path_exists(dir, depart_file_name)
    if not exists:
        dir = join_path([p.get_pre_period_info()])
        exists, file_path = file_path_exists(dir, depart_file_name)
        if not exists:
            raise ValueError(f"获取{file_path}文件出错")
        # 复制文件
        copy_file(file_path, dst_filepath)


def load_period():
    return Period()


def load_depart(period):
    return Departs(period)


def load_person_info(period):
    return BwSalaryPersons(period)


def load_data():
    p = load_period()
    period = p.get_period_info()
    departs = load_depart(period=period)
    persons = load_person_info(period=period)
    gzs = SalaryGzs(period, departs)
    jjs = SalaryJjs(period, departs)
    banks = SalaryBanks(period, departs)
    tax = SalaryTaxs(period, departs.tax_departs())
    taxOne = SalaryOneTaxs(period, departs.tax_departs())
    gjjs = SalaryGjj(period, departs)
    return p, departs, persons, gzs, jjs, banks, tax, taxOne, gjjs


def contact_info(gzs=None, jjs=None, banks=None, jobs=None, persons=None, tax=None, taxOne=None, departs=None, gjjs=None):
    df = merge_gz_and_jj(gzs, jjs)
    df = contact_id_info(df, persons)
    df = contact_bank_info(df, banks)
    df = contact_tax_info(df, tax)
    df = contact_tax_one_info(df, taxOne)
    df = contact_tax_validate(df)
    df = contact_gjj_info(df, gjjs)
    df = contact_gjj_validate(df, departs)
    return df


def contact_gjj_info(df, gjjs):
    if gjjs.df.empty:
        return df
    gjj_column = get_column_name(SalaryGjj.name, '公积金方案')
    gjj_df = gjjs.df[[utils.code_info_column_name,
                      utils.tax_column_name, gjj_column]]
    return pd.merge(df, gjj_df, on=[
        utils.code_info_column_name, utils.tax_column_name], how='left')


def contact_gjj_validate(df, departs):
    df[utils.gjj_v_column_name] = df.apply(lambda x: departs.get_bw__gjj_fangan(
        x[utils.tax_column_name], x[get_column_name(SalaryGjj.name, '公积金方案')], x[utils.depart_display_column_name]), axis=1)
    return df.copy()


def contact_id_info(df, persons):
    if persons.df.empty:
        return df
    id_df = persons.df[[code_info_column_name, tax_column_name, get_column_name(
        persons.name, person_id_column_name), get_column_name(
        persons.name, "手机号码"), get_column_name(
        persons.name, "人员类型"), get_column_name(
        persons.name, "在职状态"), get_column_name(
        persons.name, "聘用形式"), get_column_name(
        persons.name, "岗位"), get_column_name(
        persons.name, "标准岗位层级"), get_column_name(
        persons.name, "岗位族群（主）")]]
    return pd.merge(df, id_df, on=[code_info_column_name, tax_column_name], how='left')


# def contact_gjj_info(df, gjjs):
#     if gjjs.df.empty:
#         return df
#     gjj_column = get_column_name(SalaryGjj.name, '公积金方案')
#     gjj_df = gjjs.df[[code_info_column_name, tax_column_name, gjj_column]]
#     return pd.merge(df, gjj_df, on=[
#         code_info_column_name, tax_column_name], how='left')


# def contact_gjj_validate(df, departs):
#     df[gjj_v_column_name] = df.apply(lambda x: departs.get_gjj_fangan(
#         x[tax_column_name], x[get_column_name(SalaryGjj.name, '公积金方案')], x[depart_display_column_name]), axis=1)
#     return df.copy()


def validator(df):
    """
    验证本期数据
    """
    val_dict = {}
    # 银行卡
    bank_v = validator_bank_info(df)
    if len(bank_v) > 0:
        val_dict = {**val_dict, **bank_v}
    # 实发小于0
    sf_v = validator_sf_info(df)
    if len(sf_v) > 0:
        val_dict = {**val_dict, **sf_v}

    # 缺少身份证信息
    id_v = validator_id_info(df)
    if len(id_v) > 0:
        val_dict = {**val_dict, **id_v}
    # 公积金方案设置错误
    gjj_v = validator_gjj(df)
    if len(gjj_v) > 0:
        val_dict = {**val_dict, **gjj_v}

    # 所得税核对
    tax_v = validator_tax_info(df)
    if len(tax_v) > 0:
        val_dict = {**val_dict, **tax_v}

    # 其他信息
    other_v = validator_other(df)
    if len(other_v) > 0:
        val_dict = {**val_dict, **other_v}
    return val_dict


def to_tax_df(df, func):
    # 将原数据转为税表格式
    t = df.rename(columns={code_info_column_name: '工号', get_column_name(
        SalaryGzs.name, name_info_column_name): '*姓名', get_column_name(BwSalaryPersons.name, "证件号码"): '*证件号码', shouru_column_name: '本期收入', '工资信息-养老保险个人额度': '基本养老保险费', '工资信息-医疗保险个人额度': '基本医疗保险费', '工资信息-失业保险个人额度': '失业保险费', '工资信息-公积金个人额度': '住房公积金', get_column_name(SalaryGzs.name, '子女教育专项附加扣除'): '累计子女教育', get_column_name(SalaryGzs.name, '继续教育专项附加扣除'): '累计继续教育', get_column_name(SalaryGzs.name, '普通住房贷款利息专项附加扣除'): '累计住房贷款利息', get_column_name(SalaryGzs.name, '住房租金专项附加扣除'): '累计住房租金', get_column_name(SalaryGzs.name, '赡养老人专项附加扣除'): '累计赡养老人', '工资信息-企业年金个人基础缴费': '企业(职业)年金', depart_column_name: '备注'})

    res = t[['工号', '*姓名', '*证件号码', '本期收入', '基本养老保险费',
             '基本医疗保险费', '失业保险费', '住房公积金', '企业(职业)年金', '备注', utils.tax_column_name, utils.depart_display_column_name]]

    res.columns = ['工号', '*姓名', '*证件号码', '本期收入', '基本养老保险费',
                   '基本医疗保险费', '失业保险费', '住房公积金', '企业(职业)年金', '备注', utils.tax_column_name, utils.depart_display_column_name]
    res[["本期收入", '基本养老保险费',
         '基本医疗保险费', '失业保险费', '住房公积金', '企业(职业)年金']] = res.apply(
        func, axis=1, result_type='expand')
    res.insert(2, column='*证件类型', value='居民身份证')
    res.insert(5, column='*本期免税收入', value=pd.NA)
    res.insert(10, column='累计子女教育', value=pd.NA)
    res.insert(11, column='累计继续教育', value=pd.NA)
    res.insert(12, column='累计住房贷款利息', value=pd.NA)
    res.insert(13, column='累计住房租金', value=pd.NA)
    res.insert(14, column='累计赡养老人', value=pd.NA)
    res.insert(16, column='商业健康保险', value=pd.NA)
    res.insert(17, column='税延养老保险', value=pd.NA)
    res.insert(18, column='其他', value=pd.NA)
    res.insert(19, column='准予扣除的捐赠额', value=pd.NA)
    res.insert(20, column='减免税额', value=pd.NA)
    return res
    # 工号	*姓名	*证件类型	*证件号码	本期收入	本期免税收入
    # 基本养老保险费	基本医疗保险费	失业保险费	住房公积金	累计子女教育	累计继续教育	累计住房贷款利息
    # 累计住房租金	累计赡养老人	企业(职业)年金	商业健康保险	税延养老保险	其他	准予扣除的捐赠额	减免税额	备注


def to_tax_df_one(df):
    t = df.rename(columns={code_info_column_name: '工号', get_column_name(
        SalaryGzs.name, name_info_column_name): '*姓名', get_column_name(BwSalaryPersons.name, "证件号码"): '*证件号码', get_column_name(
        SalaryJjs.name, '年底兑现奖'): '*全年一次性奖金额', depart_column_name: '备注'})
    res = t[['工号', '*姓名', '*证件号码', '*全年一次性奖金额',  '备注',
             utils.tax_column_name, utils.depart_display_column_name]]
    res.insert(2, column='*证件类型', value='居民身份证')
    res.insert(5, column='免税收入', value=pd.NA)
    res.insert(6, column='其他', value=pd.NA)
    res.insert(7, column='准予扣除的捐赠额', value=pd.NA)
    res.insert(8, column='减免税额', value=pd.NA)
    res = res[res['*全年一次性奖金额'] > 0]
    return res


def to_salary_pay(period, departs, df):
    pdf_gen.create_pdf_new(period, departs, df)
    pass


def export_by_depart_type(df, period, departs, filename='导出文件', sheetname='Sheet1', depart_type=depart_display_column_name):
    for depart in departs:
        file_dir = get_export_path(period, [depart])
        file_name = f"{period}_{depart}_{filename}.xlsx"
        depart_df = split_by_depart_type(df, depart, depart_type)
        if not depart_df.empty:
            file_p = file_path(file_dir, file_name)
            depart_df.to_excel(file_p, sheet_name=sheetname, index=False)


def split_by_depart_type(df, depart, depart_type):
    res = df[df[depart_type] == depart]
    if not res.empty:
        return res.iloc[:, :-2]
    return pd.DataFrame()


class BwSalaryPersons(SalaryBaseInfo):
    """
    发薪人员信息
    """
    name = '人员信息导出结果'

    def __init__(self, period) -> None:
        super().__init__(period)
        self.name = '人员信息导出结果'
        super().get_infos()
