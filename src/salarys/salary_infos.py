#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   salary_infos.py
@Time    :   2021/10/26 10:35:53
@Author  :   Tong tan 
@Version :   1.0
@Contact :   tongtan@gmail.com
'''


from os import name

from numpy import column_stack
import src.salarys.data_read as prx
import src.salarys.utils as utils


class SalaryBaseInfo:
    def __init__(self, period) -> None:
        self.period = period
        if not self.period:
            raise ValueError(f'请指定期间信息')
        self.name = ''
        self.file_sub_dir = []
        self.df = None
        self.group_by = []
        self.skip_err = True
        self.err_paths = []

    def get_group_by_columns_info(self):
        return [get_column_name(self.name, col) for col in self.group_by]

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
            self.df[get_column_name(
                self.name, utils.tax_column_name)] = split_depart_infos(departs)
            self.df[get_column_name(
                self.name, utils.depart_column_name)] = split_depart_infos(departs, 1)
            self.df[get_column_name(
                self.name, utils.depart_display_column_name)] = get_depart_display_info()

    def get_infos(self):
        self.get_df_and_err_paths()
        self.rename_columns()
        self.append_tax_name_and_display_name()
        if len(self.group_by) > 0:
            prx.group_by_columns(self.df, self.get_group_by_columns_info())

        self.df.to_excel(f'{self.name}{utils.column_name_sep}x.xlsx')


class SalaryGzs(SalaryBaseInfo):
    """
    工资信息
    """

    def __init__(self, period) -> None:
        super().__init__(period)
        self.name = '工资信息'
        self.file_sub_dir = [utils.gz_jj_dir]
        super().get_infos()


class SalaryJjs(SalaryBaseInfo):
    """
    奖金信息
    """

    def __init__(self, period) -> None:
        super().__init__(period)
        self.name = '奖金信息'
        self.file_sub_dir = [utils.gz_jj_dir]
        self.group_by = [utils.tax_column_name,
                         utils.depart_column_name, utils.code_info_column_name]
        super().get_infos()


class SalaryBanks(SalaryBaseInfo):
    """
    银行卡信息
    """

    def __init__(self, period) -> None:
        super().__init__(period)
        self.name = '银行卡信息'
        super().get_infos()


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

    def __init__(self, period) -> None:
        super().__init__(period)
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
        self.get_taxs_infos()

    def tax_name(self):
        return f'{self.period}_税款计算_工资薪金所得'

    def get_taxs_infos(self):
        if not self.df:
            r = dict()
            for tax_depart in self.tax_departs:
                df, _ = prx.make_df_from_excel_files(
                    period=self.period, file_root_path=utils.root_dir_(), file_sub_path=[utils.tax_dir, tax_depart], file_name_prefix=self.name)
                if not df.empty:
                    r[tax_depart] = df


def split_depart_infos(departs, no=0):
    return list(map(lambda s: s.split(
        utils.depart_info_sep)[no], departs))


def get_depart_display_info():
    pass


def get_column_name(prefix, column_name):
    return f'{prefix}{utils.column_name_sep}{column_name}'
