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
            columns={'通行证': utils.code_info_column_name}, inplace=True)
        self.df.rename(
            columns={'部门': utils.depart_info_column_name}, inplace=True)
        self.df.rename(
            columns={'机构名称': utils.depart_info_column_name}, inplace=True)

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

        # 导出
        # self.df.to_excel(f'{self.name}{utils.column_name_sep}x.xlsx')


class SalaryGzs(SalaryBaseInfo):
    """
    工资信息
    """

    def __init__(self, period, departs) -> None:
        super().__init__(period, departs)
        self.name = '工资信息'
        self.file_sub_dir = [utils.gz_jj_dir]
        super().get_infos()


class SalaryJjs(SalaryBaseInfo):
    """
    奖金信息
    """

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

    def __init__(self, period, departs) -> None:
        super().__init__(period, departs)
        self.name = '银行卡信息'
        self.converters = {'卡号': str}
        super().get_infos()
        self.df = self.split_by_bank_purpose()

        # self.export_some_columns(['卡号_x', '卡号_y'])

    def split_by_bank_purpose(self):
        gz_bank_df = self.df[self.df[get_column_name(
            self.name, "卡用途")].str.contains('工资卡') == True]
        jj_bank_df = self.df[(self.df[get_column_name(
            self.name, "卡用途")].str.contains('奖金卡')) == True]
        return pd.merge(gz_bank_df, jj_bank_df, on=[get_column_name(self.name, utils.code_info_column_name), utils.depart_display_column_name])

    # def export_some_columns(self, export_columns=[]):
    #     df = self.df[list(
    #         map(lambda x:get_column_name(self.name, x), export_columns))]
    #     return df.to_excel('f.xlsx')


class SalaryPersons(SalaryBaseInfo):
    """
    发薪人员信息
    """

    def __init__(self, period) -> None:
        super().__init__(period)
        self.name = '人员信息导出结果'
        super().get_infos()


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


def split_depart_infos(departs, no=0):
    return list(map(lambda s: s.split(
        utils.depart_info_sep)[no], departs))


def get_depart_display_info(depart_infos, departs):
    if departs:
        return list(map(lambda s: departs.display_depart_name(s[0], s[1]), depart_infos))


def get_column_name(prefix, column_name):
    if column_name == utils.code_info_column_name:
        return column_name
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
    return period, ds, gzs, jjs, banks, jobs, persons


def merge_gz_and_jj(gz_infos, jj_infos):
    df = pd.merge(gz_infos.df, jj_infos.df, on=[
                  utils.code_info_column_name, utils.tax_column_name, utils.depart_display_column_name], how='outer', suffixes=['_工资', '_奖金'])
    return df


def contact_id_info(df, persons):
    id_df = persons.df[[utils.code_info_column_name, get_column_name(
        persons.name, utils.person_id_column_name)]]
    s = pd.merge(df, id_df, on=[utils.code_info_column_name], how='outer')
    return s


def contact_bank_info(df, banks):
    bank_df = df.df[[utils.code_info_column_name, get_column_name(
        banks.name, utils.person_id_column_name)]]


def append_code_and_id_and_bank_and_tax_and_job(df, persons, banks, jobs):
    df['员工编码'] = list(map(lambda x: x[1] if pd.isna(x[0]) else x[0],
                          df[['工资信息-员工通行证', '奖金信息-员工通行证']].values))
    df['身份证号'] = list(map(lambda x: get_value(persons, x, "证件号码"),
                          df['员工编码'].values.tolist()))
    df['手机号码'] = list(map(lambda x: get_value(persons, x, "手机号码"),
                          df['员工编码'].values.tolist()))
    df['岗位类型'] = list(map(lambda x: get_value(jobs, x, "岗位类型"),
                          df['员工编码'].values.tolist()))
    df['岗位名称'] = list(map(lambda x: get_value(jobs, x, "执行岗位名称"),
                          df['员工编码'].values.tolist()))
    df['岗位层级'] = list(map(lambda x: get_value(jobs, x, "岗位层级"),
                          df['员工编码'].values.tolist()))
    df['组合(岗位序列+标准目录+岗位层级)'] = list(map(lambda x: get_value(jobs, x, "组合(岗位序列+标准目录+岗位层级)"),
                                        df['员工编码'].values.tolist()))
    # df['岗位类型'] = list(map(lambda x: get_value(jobs, x，"岗位类型"),
    #                       df['员工编码'].values.tolist()))
    # df.tail(200).to_excel('x.xlsx')


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
