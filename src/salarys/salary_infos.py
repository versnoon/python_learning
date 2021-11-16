#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   salary_infos.py
@Time    :   2021/10/26 10:35:53
@Author  :   Tong tan
@Version :   1.0
@Contact :   tongtan@gmail.com
'''


import pandas as pd
from pandas.core.frame import DataFrame
import src.salarys.data_read as prx
import src.salarys.utils as utils
import src.salarys.period as period_op
import src.salarys.depart as depart_op


class SalaryBaseInfo:
    def __init__(self, period, departs=None) -> None:
        self.period = period
        self.departs = departs
        if not self.period:
            raise ValueError(f'请指定期间信息')
        self.name = ''
        self.file_sub_dir = []
        self.df = None
        self.group_by = []
        self.converters = {}
        self.skip_err = True
        self.err_paths = []

    def get_group_by_columns_info(self):
        return [col for col in self.group_by]

    def get_df_and_err_paths(self):
        if not self.df:
            self.df, self.err_paths = prx.make_df_from_excel_files(
                period=self.period, file_root_path=utils.root_dir_(), file_sub_path=self.file_sub_dir, file_name_prefix=self.name)
            if not self.skip_err:
                err_file_msg = '|'.join(self.err_paths)
                if err_file_msg:
                    err_file_msg = f'获取数据出错，错误信息:[{err_file_msg}]文件数据内容为空，或者文件不存在'
                else:
                    err_file_msg = f'获取数据出错，错误信息:[{self.name}]相关数据文件不存在'
                raise ValueError(err_file_msg)

    def rename_columns(self):

        # 规范关键字段的字段名称
        self.df.rename(
            columns={'通行证': utils.code_info_column_name, '部门': utils.depart_info_column_name, '机构名称': utils.depart_info_column_name}, inplace=True)

        self.df.rename(columns=lambda x: get_column_name(
            self.name, x), inplace=True)

    def append_tax_name_and_display_name(self):
        columns = self.df.columns.tolist()
        depart_column_name = get_column_name(
            self.name, utils.depart_info_column_name)
        if depart_column_name in columns:
            departs = self.df[depart_column_name].values.tolist()
            tax_name = utils.tax_column_name
            self.df[tax_name] = split_depart_infos(departs)
            depart_name = utils.depart_column_name
            self.df[depart_name] = split_depart_infos(departs, 1)

            depart_infos = self.df[[tax_name, depart_name]].values.tolist()
            self.df[utils.depart_display_column_name] = get_depart_display_info(
                depart_infos, self.departs)

    def get_infos(self):
        # 读取
        self.get_df_and_err_paths()
        # 列明规范化
        self.rename_columns()
        # 增加税组单位等信息
        self.append_tax_name_and_display_name()
        # 分组合计
        if len(self.group_by) > 0:
            prx.group_by_columns(self.df, self.get_group_by_columns_info())


class SalaryGzs(SalaryBaseInfo):
    """
    工资信息
    """
    name = '工资信息'

    def __init__(self, period, departs) -> None:
        super().__init__(period, departs)
        self.name = '工资信息'
        self.file_sub_dir = [utils.gz_jj_dir]
        super().get_infos()


class SalaryJjs(SalaryBaseInfo):
    """
    奖金信息
    """
    name = '奖金信息'

    def __init__(self, period, departs) -> None:
        super().__init__(period, departs)
        self.name = '奖金信息'
        self.file_sub_dir = [utils.gz_jj_dir]
        self.group_by = [utils.tax_column_name,
                         utils.depart_column_name, utils.code_info_column_name]
        super().get_infos()


class SalaryBanks(SalaryBaseInfo):
    """
    银行卡信息
    """
    name = '银行卡信息'

    def __init__(self, period, departs) -> None:
        super().__init__(period, departs)
        self.name = '银行卡信息'
        self.converters = {'卡号': str}
        super().get_infos()
        self.df = self.split_by_bank_purpose()

        # self.export_some_columns(['卡号_x', '卡号_y'])

    def split_by_bank_purpose(self):
        if not self.df.empty:
            gz_bank_df = self.df[self.df[get_column_name(
                self.name, "卡用途")].str.contains('工资卡') == True]
            jj_bank_df = self.df[(self.df[get_column_name(
                self.name, "卡用途")].str.contains('奖金卡')) == True]
            return pd.merge(gz_bank_df, jj_bank_df, on=[get_column_name(self.name, utils.code_info_column_name), utils.tax_column_name, utils.depart_display_column_name], how='outer', suffixes=[f"{utils.column_name_suffix_sep}工资卡", f"{utils.column_name_suffix_sep}奖金卡"])
        return pd.DataFrame()
    # def export_some_columns(self, export_columns=[]):
    #     df = self.df[list(
    #         map(lambda x:get_column_name(self.name, x), export_columns))]
    #     return df.to_excel('f.xlsx')


class SalaryPersons(SalaryBaseInfo):
    """
    发薪人员信息
    """
    name = '人员信息导出结果'

    def __init__(self, period) -> None:
        super().__init__(period)
        self.name = '人员信息导出结果'
        super().get_infos()
        self.df.drop_duplicates(get_column_name(
            self.name, utils.code_info_column_name), inplace=True)


class SalaryPersonJobs(SalaryBaseInfo):
    """
    发薪人员岗位信息
    """

    def __init__(self, period, departs) -> None:
        super().__init__(period, departs)
        self.name = '岗位聘用信息'
        super().get_infos()


class SalaryTaxs(SalaryBaseInfo):
    """
    发薪人员税务信息
    """

    def __init__(self, period, tax_departs=[]) -> None:
        super().__init__(period)
        self.tax_departs = tax_departs
        self.name = self.tax_name()
        self.get_tax()

    def tax_name(self):
        return f'{self.period}_税款计算_工资薪金所得'

    def get_tax(self):
        if not self.df:
            chunks = []
            for tax_depart in self.tax_departs:
                df, _ = prx.make_df_from_excel_files(
                    period=self.period, file_root_path=utils.root_dir_(), file_sub_path=[utils.tax_dir, tax_depart], file_name_prefix=self.name)
                if not df.empty:
                    tax_name = utils.tax_column_name
                    df[tax_name] = tax_depart
                    chunks.append(df)
            if len(chunks) > 0:
                self.df = pd.concat(chunks, ignore_index=True)
            else:
                self.df = pd.DataFrame()


def split_depart_infos(departs, no=0):
    return list(map(lambda s: s.split(
        utils.depart_info_sep)[no], departs))


def get_depart_display_info(depart_infos, departs):
    if departs:
        return list(map(lambda s: departs.display_depart_name(s[0], s[1]), depart_infos))


def get_column_name(prefix, column_name, suffix=""):
    if column_name == utils.code_info_column_name:
        return column_name
    if suffix:
        column_name = add_column_name_suffix(column_name, suffix)
    return f'{prefix}{utils.column_name_sep}{column_name}'


def add_column_name_suffix(column_name, suffix):
    return f'{column_name}{utils.column_name_suffix_sep}{suffix}'


def load_data_to_frame():
    p = period_op.Period()
    period = p.get_period_info()
    ds = depart_op.Departs(period=period)
    gzs = SalaryGzs(period, departs=ds)
    jjs = SalaryJjs(period, departs=ds)
    banks = SalaryBanks(period, departs=ds)
    jobs = SalaryPersonJobs(period, departs=ds)
    persons = SalaryPersons(period)
    tax = SalaryTaxs(period, ds.tax_departs())
    return period, ds, gzs, jjs, banks, jobs, persons, tax


def contact_info(gzs, jjs, banks, jobs, persons, tax):
    df = merge_gz_and_jj(gzs, jjs)
    df = contact_id_info(df, persons)
    df = contact_bank_info(df, banks)
    df = contact_job_info(df, jobs)
    df = contact_tax_info(df, tax)
    return df


def validator(df):
    """
    验证本期数据
    """
    val_dict = {}
    # writer = pd.ExcelWriter('效验结果.xlsx')
    # 实发小于0
    if get_column_name(SalaryGzs.name, "实发") in df.columns:
        res = df[(df[get_column_name(SalaryGzs.name, "实发")].notna(
        )) & (df[get_column_name(SalaryGzs.name, "实发")] < 0)]
        if not res.empty:
            val_dict['工资实发小于0'] = res.copy()
    if get_column_name(SalaryJjs.name, "实发") in df.columns:
        res = df[(df[get_column_name(SalaryJjs.name, "实发")].notna(
        )) & (df[get_column_name(SalaryJjs.name, "实发")] < 0)]
        if not res.empty:
            val_dict['奖金实发小于0'] = res.copy()
    if get_column_name(SalaryGzs.name, "实发") in df.columns and get_column_name(SalaryBanks.name, "卡号", "工资卡") in df.columns:
        res = df[(df[get_column_name(SalaryGzs.name, "实发")].notna()) & (df[get_column_name(
            SalaryGzs.name, "实发")] > 0) & (df[get_column_name(SalaryBanks.name, "卡号", "工资卡")].isna())]
        if not res.empty:
            val_dict['缺少工资卡信息'] = res.copy()
    if get_column_name(SalaryJjs.name, "实发") in df.columns and get_column_name(SalaryBanks.name, "卡号", "奖金卡") in df.columns:
        res = df[(df[get_column_name(SalaryJjs.name, "实发")].notna()) & (df[get_column_name(
            SalaryJjs.name, "实发")] > 0) & (df[get_column_name(SalaryBanks.name, "卡号", "奖金卡")].isna())]
        if not res.empty:
            val_dict['缺少奖金卡信息'] = res.copy()
    # 所得税核对
    if "所得税" in df.columns and "累计应补(退)税额" in df.columns:
        res = df[df.loc[:, ["所得税", "累计应补(退)税额"]].sum(axis=1).round(0) != 0]
        res = res.copy()
        res.loc[:, "个税调整_值"] = 0 - \
            df.loc[:, ["所得税", "累计应补(退)税额"]].sum(axis=1).round(2)
        if not res.empty:
            val_dict['个税错误信息'] = res.copy()

    if get_column_name(SalaryGzs.name, "薪酬模式") in df.columns and get_column_name(SalaryGzs.name, "岗位工资") in df.columns:
        # 缺少岗位工资
        res = df[(df[get_column_name(SalaryGzs.name, "薪酬模式")] ==
                  '岗位绩效工资制') & (df[get_column_name(SalaryGzs.name, "岗位工资")] == 0)]
        if not res.empty:
            val_dict['岗位工资错误信息'] = res.copy()
        # 离岗休息实发未0验证
        res = df[(df[get_column_name(SalaryGzs.name, "薪酬模式")] ==
                  '生活费（2021年离岗休息）') & (df[get_column_name(SalaryGzs.name, "生活补贴")] == 0) & (df[get_column_name(SalaryGzs.name, "实发")] != 0)]
        if not res.empty:
            val_dict['自主创业错误信息'] = res.copy()
         # 只管领导验证，防止跨年年功工资计算出值
        res = df[(df[get_column_name(SalaryGzs.name, "薪酬模式")] ==
                  '总部直管领导年薪制') & ((df[get_column_name(SalaryGzs.name, "工龄工资")].notna()) | (df[get_column_name(SalaryGzs.name, "岗位工资")].notna()))]
        if not res.empty:
            val_dict['经营层薪酬错误信息'] = res.copy()
    # 缺少身份证信息
    if get_column_name(SalaryPersons.name, utils.person_id_column_name) in df.columns and utils.yingfa_column_name in df.columns:
        res = df[(df[utils.yingfa_column_name] > 0) & (
            df[get_column_name(SalaryPersons.name, utils.person_id_column_name)].isna())]
        if not res.empty:
            val_dict['身份证错误信息'] = res.copy()
    return val_dict


def get_export_path(period, paths=[]):
    ps = [period]
    ps.extend(paths)
    return utils.join_path(ps)


def export_all_errs(period, errs):
    file_dir = get_export_path(period, ['汇总数据'])
    file_name = f"{period}_效验结果.xlsx"
    writer = pd.ExcelWriter(utils.file_path(file_dir, file_name))
    for name, df in errs.items():
        df.to_excel(writer, name)
    writer.save()


def export_errs_by_display_depart(period, errs, departs):
    for depart in departs:
        file_dir = get_export_path(period, [depart])
        file_name = f"{period}_{depart}_效验结果.xlsx"

        depart_err = split_by_display_depart(errs, depart)
        if len(depart_err) > 0:
            writer = pd.ExcelWriter(utils.file_path(file_dir, file_name))
            for name, df in depart_err.items():
                df.to_excel(writer, name)
            writer.save()


def split_by_display_depart(errs, depart):
    res = {}
    for name, df in errs.items():
        depart_df = df[df[utils.depart_display_column_name] == depart]
        if not depart_df.empty:
            res[name] = depart_df
    return res


def merge_gz_and_jj(gz_infos, jj_infos):
    if not gz_infos.df.empty and not jj_infos.df.empty:
        df = pd.merge(gz_infos.df, jj_infos.df, on=[
            utils.code_info_column_name, utils.tax_column_name, utils.depart_display_column_name], how='outer', suffixes=['_工资', '_奖金'], copy=True)
        append_yingf_shif_shui(df)
        return df
    elif not gz_infos.df.empty and jj_infos.df.empty:
        return gz_infos.df
    elif gz_infos.df.emtpy and not jj_infos.df.empty:
        return jj_infos.df


def append_yingf_shif_shui(df):

    df[utils.yingfa_column_name] = df[get_column_name(
        SalaryGzs.name, "应发")].add(df[get_column_name(SalaryJjs.name, "应发")], fill_value=0)
    df[utils.shifa_column_name] = df[get_column_name(
        SalaryGzs.name, "实发")] .add(df[get_column_name(SalaryJjs.name, "实发")], fill_value=0)
    if get_column_name(SalaryJjs.name, "个税调整") in df.columns:
        df[utils.suodeshui_column_name] = (df.loc[:, [get_column_name(
            SalaryGzs.name, "个调税"), get_column_name(SalaryJjs.name, "个调税"), get_column_name(SalaryJjs.name, "个税调整")]].sum(axis=1))
    else:
        df[utils.suodeshui_column_name] = (df.loc[:, [get_column_name(
            SalaryGzs.name, "个调税"), get_column_name(SalaryJjs.name, "个调税")]].sum(axis=1))
    return df


def contact_id_info(df, persons):
    if persons.df.empty:
        return df
    id_df = persons.df[[utils.code_info_column_name, get_column_name(
        persons.name, utils.person_id_column_name), get_column_name(
        persons.name, "手机号码"), get_column_name(
        persons.name, "人员类型"), get_column_name(
        persons.name, "在职状态"), get_column_name(
        persons.name, "参加工作时间")]]
    s = pd.merge(df, id_df, on=[utils.code_info_column_name], how='left')
    return s


def contact_bank_info(df, banks):
    if banks.df.empty:
        return df
    if not banks.df.empty:
        bank_df = banks.df[[utils.code_info_column_name,  utils.tax_column_name, utils.depart_display_column_name, get_column_name(
            banks.name, "金融机构", "工资卡"), get_column_name(
            banks.name, "卡号", "工资卡"), get_column_name(
            banks.name, "金融机构", "奖金卡"), get_column_name(
            banks.name, "卡号", "奖金卡")]]
        s = pd.merge(df, bank_df, on=[
            utils.code_info_column_name, utils.tax_column_name, utils.depart_display_column_name], how='left')
        return s


def contact_job_info(df, jobs):
    if jobs.df.empty:
        job_df = jobs.df[[utils.code_info_column_name,  utils.tax_column_name, utils.depart_display_column_name, get_column_name(
            jobs.name, "岗位类型"), get_column_name(
            jobs.name, "执行岗位名称"), get_column_name(
            jobs.name, "岗位层级"), get_column_name(
            jobs.name, "组合(岗位序列+标准目录+岗位层级)")]]
        s = pd.merge(df, job_df, on=[
            utils.code_info_column_name, utils.tax_column_name, utils.depart_display_column_name], how='left')
        return s
    else:
        return df


def contact_tax_info(df, tax):
    if not tax.df.empty:
        tax_df = tax.df[[utils.person_id_column_name,
                         utils.tax_column_name, "累计应补(退)税额"]]
        df.loc[:, f'人员信息导出结果-证件号码_lower'] = df['人员信息导出结果-证件号码'].str.lower()
        tax_df.loc[:, f'{utils.person_id_column_name}_lower'] = tax_df[utils.person_id_column_name].str.lower()
        s = pd.merge(df, tax_df, left_on=["人员信息导出结果-证件号码_lower", utils.tax_column_name], right_on=[
            f'{utils.person_id_column_name}_lower', utils.tax_column_name], how='outer')
        return s
    else:
        return df


# def append_code_and_id_and_bank_and_tax_and_job(df, persons, banks, jobs):
""""""
#    速度太慢
#    df['员工编码'] = list(map(lambda x: x[1] if pd.isna(x[0]) else x[0],
#                           df[['工资信息-员工通行证', '奖金信息-员工通行证']].values))
#     df['身份证号'] = list(map(lambda x: get_value(persons, x, "证件号码"),
#                           df['员工编码'].values.tolist()))
#     df['手机号码'] = list(map(lambda x: get_value(persons, x, "手机号码"),
#                           df['员工编码'].values.tolist()))
#     df['岗位类型'] = list(map(lambda x: get_value(jobs, x, "岗位类型"),
#                           df['员工编码'].values.tolist()))
#     df['岗位名称'] = list(map(lambda x: get_value(jobs, x, "执行岗位名称"),
#                           df['员工编码'].values.tolist()))
#     df['岗位层级'] = list(map(lambda x: get_value(jobs, x, "岗位层级"),
#                           df['员工编码'].values.tolist()))
#     df['组合(岗位序列+标准目录+岗位层级)'] = list(map(lambda x: get_value(jobs, x, "组合(岗位序列+标准目录+岗位层级)"),
#                                         df['员工编码'].values.tolist()))
#     # df['岗位类型'] = list(map(lambda x: get_value(jobs, x，"岗位类型"),
#     #                       df['员工编码'].values.tolist()))
#     # df.tail(200).to_excel('x.xlsx')


def get_value(df, name, code, c_name):
    return get_value_with_suffix(df, name, code, c_name, "")


def get_value_with_suffix(df, name, code, c_name, suffix):
    p_df = df[df[utils.code_info_column_name] == code]
    if p_df.empty:
        return ""
    if suffix:
        c_name = add_column_name_suffix(c_name, suffix)
    key = c_name
    if name:
        key = get_column_name(name, c_name)
    d = p_df[key]
    return d.values[0]


def to_sap_frame(df):
    """
    把宝武ehr相关项目转为sap对应的项目名称和排序
    """
    sap_df = pd.DataFrame()
    # 添加缺失项目
    sap_df["实发核对"] = 0
    sap_df["一级组织"]
    pass
