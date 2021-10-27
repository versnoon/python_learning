#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   salary_infos.py
@Time    :   2021/10/26 10:35:53
@Author  :   Tong tan 
@Version :   1.0
@Contact :   tongtan@gmail.com
'''


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
        self.skip_err = True
        self.err_paths = []

    def get_infos(self):
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


class SalaryGzs(SalaryBaseInfo):
    """
    工资信息
    """

    def __init__(self, period) -> None:
        super().__init__(period)
        self.name = '工资信息'
        self.file_sub_dir = [utils.gz_jj_dir]
        super().get_infos()
        self.df.rename(columns={f'{self.name}': '', '': ''}, inplace=True)


class SalaryJjs(SalaryBaseInfo):
    """
    奖金信息
    """

    def __init__(self, period) -> None:
        super().__init__(period)
        self.name = '奖金信息'
        self.file_sub_dir = [utils.gz_jj_dir]
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
        self.dfs = dict()
        self.get_taxs_infos()

    def tax_name(self):
        return f'{self.period}_税款计算_工资薪金所得'

    def get_taxs_infos(self):
        if not self.df:
            for tax_depart in self.tax_departs:
                df, _ = prx.make_df_from_excel_files(
                    period=self.period, file_root_path=utils.root_dir_(), file_sub_path=[utils.tax_dir, tax_depart], file_name_prefix=self.name)
                if not df.empty:
                    self.dfs[tax_depart] = df


def get_column_name(prefix, column_name):
    return f'{prefix}{utils.column_name_sep}{column_name}'
