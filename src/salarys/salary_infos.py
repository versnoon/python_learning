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
from pandas._libs.missing import NA
import src.salarys.data_read as prx
import src.salarys.utils as utils
import src.salarys.period as period_op
import src.salarys.depart as depart_op


def sub_nddx(x):
    if not x.empty:
        print(x)


def depart_info_map(x):
    if isinstance(x, str) and not pd.isna(x):
        departs = x.split("\\")
        first = 0
        for i, d in enumerate(departs):
            if "总部" in d:
                first = i
                break
        return "\\".join(departs[first:])
    return x


def gts(x):
    if not pd.isna(x):
        return round(0 - x, 2)
    return 0


def bank_card_no(x):
    return f'{x}_'


class SalaryBaseInfo:
    def __init__(self, period, departs=None) -> None:
        self.period = period
        self.departs = departs
        if not self.period:
            raise ValueError(f'请指定期间信息')
        self.name = ''
        self.file_sub_dir = []
        self.df = pd.DataFrame()
        self.group_by = []
        self.converters = {}
        self.skip_err = True
        self.err_paths = []

    def get_group_by_columns_info(self):
        return [col for col in self.group_by]

    def get_df_and_err_paths(self):
        if self.df.empty:
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
            columns={'宝武通行证': utils.code_info_column_name, '通行证': utils.code_info_column_name, '工号': utils.code_info_column_name, '部门': utils.depart_info_column_name, '所在机构': utils.depart_info_column_name, '所属机构': utils.depart_info_column_name, '机构名称': utils.depart_info_column_name, '银行卡号': '卡号', '企业年金个人额度': '企业年金个人基础缴费'},  inplace=True)

        self.df.rename(columns=lambda x: get_column_name(
            self.name, x), inplace=True)

    def standant_depart_info(self):
        # 规范机构信息
        d_name = get_column_name(self.name, utils.depart_info_column_name)
        if d_name in self.df.columns:
            self.df.loc[:, d_name] = self.df[d_name].apply(depart_info_map)

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
        # 读取后做其他操作
        self.do_after_load_data()
        # 列明规范化
        self.rename_columns()
        # 去除机构信息中总部以前的机构信息
        self.standant_depart_info()
        # 增加税组单位等信息
        self.append_tax_name_and_display_name()
        # 分组合计
        if len(self.group_by) > 0:
            self.df = prx.group_by_columns(
                self.df, self.get_group_by_columns_info())

    def do_after_load_data(self):
        pass


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

    def do_after_load_data(self):
        if not self.df.empty:
            pass
            # if "养老保险个人额度" in self.df.columns:
            #     if self.df["养老保险个人额度"] < 0:
            #         self.df["养老保险个人额度"] = self.df["养老保险个人额度"].abs()
            # if "失业保险个人额度" in self.df.columns:
            #     if self.df["失业保险个人额度"] < 0:
            #         self.df["失业保险个人额度"] = self.df["失业保险个人额度"].abs()
            # if "医疗保险个人额度" in self.df.columns:
            #     if self.df["医疗保险个人额度"] < 0:
            #         self.df["医疗保险个人额度"] = self.df["医疗保险个人额度"].abs()
            # if "公积金个人额度" in self.df.columns:
            #     if self.df["公积金个人额度"] < 0:
            #         self.df["公积金个人额度"] = self.df["公积金个人额度"].abs()
            # if "企业年金个人额度" in self.df.columns:
            #     if self.df["企业年金个人额度"] < 0:
            #         self.df["企业年金个人额度"] = self.df["企业年金个人额度"].abs()


class SalaryJjs(SalaryBaseInfo):
    """
    奖金信息
    """
    name = '奖金信息'

    def __init__(self, period, departs) -> None:
        super().__init__(period, departs)
        self.name = '奖金信息'
        self.file_sub_dir = [utils.gz_jj_dir]
        self.group_by = [utils.tax_column_name, get_column_name(self.name, utils.name_info_column_name), get_column_name(self.name, utils.depart_info_column_name),
                         utils.depart_display_column_name, utils.code_info_column_name]
        super().get_infos()


class SalaryBanks(SalaryBaseInfo):
    """
    银行卡信息
    """
    name = '银行卡信息'

    def __init__(self, period, departs) -> None:
        super().__init__(period, departs)
        self.name = '银行卡信息'
        self.dtypes = {'卡号': str, '银行卡号': str}
        super().get_infos()
        self.standant_card_info()
        self.df = self.split_by_bank_purpose()

        # self.export_some_columns(['卡号_x', '卡号_y'])

    def standant_card_info(self):
        # 规范机构信息
        card_name = get_column_name(self.name, '卡号')
        if card_name in self.df.columns:
            self.df.loc[:, card_name] = self.df[card_name].apply(
                bank_card_no)

    def split_by_bank_purpose(self):
        if not self.df.empty:
            gz_bank_df = self.df[(self.df[get_column_name(
                self.name, "卡用途")].str.contains('工资')) & (self.df[get_column_name(
                    self.name, "卡号")].notna())]
            gz_bank_df.drop_duplicates(
                subset=[utils.code_info_column_name, utils.tax_column_name, utils.depart_display_column_name], inplace=True)
            jj_bank_df = self.df[((self.df[get_column_name(
                self.name, "卡用途")].str.contains('奖金'))) & (self.df[get_column_name(
                    self.name, "卡号")].notna())]
            jj_bank_df.drop_duplicates(
                subset=[utils.code_info_column_name, utils.tax_column_name, utils.depart_display_column_name], inplace=True)
            t = pd.merge(gz_bank_df, jj_bank_df, on=[utils.code_info_column_name, utils.tax_column_name, utils.depart_display_column_name], how='outer', suffixes=[
                         f"{utils.column_name_suffix_sep}工资卡", f"{utils.column_name_suffix_sep}奖金卡"])
            t.drop_duplicates(
                subset=[utils.code_info_column_name, utils.tax_column_name], inplace=True)
            return t
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
        self.df.drop_duplicates(utils.code_info_column_name, inplace=True)

    def do_after_load_data(self):
        if not self.df.empty:
            if '工号' in self.df.columns:
                self.df.rename(
                    columns={'工号': '工号_1'},  inplace=True)


class SalaryPersonJobs(SalaryBaseInfo):
    """
    发薪人员岗位信息
    """
    name = '岗位聘用信息'

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
        if self.df.empty:
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


class SalaryOneTaxs(SalaryTaxs):
    def __init__(self, period, tax_departs=[]) -> None:
        super().__init__(period)
        self.tax_departs = tax_departs
        self.name = self.tax_name()
        self.get_tax()

    def tax_name(self):
        return f'{self.period}_税款计算_全年一次性奖金收入'


class SalaryGjj(SalaryBaseInfo):
    """
    发薪人员公积金数据
    """
    name = '公积金信息'

    def __init__(self, period, departs) -> None:
        super().__init__(period, departs)
        self.file_sub_dir = [utils.insurance_dir]
        self.name = '公积金信息'
        super().get_infos()


def split_depart_infos(departs, no=0):
    return list(map(lambda s:  s.split(
        utils.depart_info_sep)[no] if not pd.isna(s) and utils.depart_info_sep in s else s, departs))


def get_depart_display_info(depart_infos, departs):
    if departs:
        return list(map(lambda s: departs.display_depart_name(s[0], s[1]) if len(s) == 2 else s[0], depart_infos))


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
    taxOne = SalaryOneTaxs(period, ds.tax_departs())
    gjjs = SalaryGjj(period, ds)
    return period, ds, gzs, jjs, banks, jobs, persons, tax, taxOne, gjjs


def contact_info(gzs=None, jjs=None, banks=None, jobs=None, persons=None, tax=None, taxOne=None, departs=None, gjjs=None):
    df = merge_gz_and_jj(gzs, jjs)
    df = contact_id_info(df, persons)
    df = contact_bank_info(df, banks)
    df = contact_job_info(df, jobs)
    df = contact_tax_info(df, tax)
    df = contact_tax_one_info(df, taxOne)
    df = contact_tax_validate(df)
    df = contact_gjj_info(df, gjjs)
    df = contact_gjj_validate(df, departs)
    return df


def contact_gjj_info(df, gjjs):
    if gjjs.df.empty:
        return df
    gjj_column = get_column_name(SalaryGjj.name, '公积金(类型)')
    gjj_df = gjjs.df[[utils.code_info_column_name,
                      utils.tax_column_name, gjj_column]]
    return pd.merge(df, gjj_df, on=[
        utils.code_info_column_name, utils.tax_column_name], how='left')


def contact_gjj_validate(df, departs):
    df[utils.gjj_v_column_name] = df.apply(lambda x: departs.get_gjj_fangan(
        x[utils.tax_column_name], x[get_column_name(SalaryGjj.name, '公积金(类型)')], x[utils.depart_display_column_name]) if get_column_name(SalaryGjj.name, '公积金(类型)') in x.index else '', axis=1)
    return df.copy()


def contact_tax_validate(df):
    if utils.tax_column_name in df.columns and '累计应补(退)税额' in df.columns:
        if utils.shouru_column_name in df.columns:
            df['个税调整_值'] = df.apply(lambda x: tax_compare(
                x[utils.suodeshui_column_name], x['累计应补(退)税额']), axis=1)
            if '累计应补(退)税额_一次性' in df.columns:
                df['个税调整_值'] = df.apply(lambda x: tax_compare(
                    x[utils.suodeshui_column_name], x['累计应补(退)税额'], x['累计应补(退)税额_一次性']), axis=1)

    return df.copy()


def tax_compare(tax1, tax2, tax_one=0):
    if pd.isna(tax1):
        tax1 = 0
    if pd.isna(tax2):
        tax2 = 0
    if pd.isna(tax_one):
        tax_one = 0
    return round(tax2 + tax_one - tax1, 2)


def validator_bank_info(df):
    val_dict = {}
    if get_column_name(SalaryGzs.name, "实发") in df.columns:
        res = df[(df[get_column_name(SalaryGzs.name, "实发")].notna(
        )) & (df[get_column_name(SalaryGzs.name, "实发")] < 0)]
        if not res.empty:
            res = export_columns(res)
            val_dict['工资实发小于0'] = res.copy()
    if get_column_name(SalaryJjs.name, "实发") in df.columns:
        res = df[(df[get_column_name(SalaryJjs.name, "实发")].notna(
        )) & (df[get_column_name(SalaryJjs.name, "实发")] < 0)]
        if not res.empty:
            res = export_columns(res)
            val_dict['奖金实发小于0'] = res.copy()
    return val_dict


def validator_sf_info(df):
    val_dict = {}
    if get_column_name(SalaryGzs.name, "实发") in df.columns and get_column_name(SalaryBanks.name, "卡号", "工资卡") in df.columns:
        res = df[(df[get_column_name(SalaryGzs.name, "实发")].notna()) & (df[get_column_name(
            SalaryGzs.name, "实发")] > 0) & (df[get_column_name(SalaryBanks.name, "卡号", "工资卡")].isna())]
        if not res.empty:
            val_dict['缺少工资卡信息'] = res.copy()
    if get_column_name(SalaryJjs.name, "实发") in df.columns and get_column_name(SalaryBanks.name, "卡号", "奖金卡") in df.columns:
        res = df[(df[get_column_name(SalaryJjs.name, "实发")].notna()) & (df[get_column_name(
            SalaryJjs.name, "实发")] > 0) & (df[get_column_name(SalaryBanks.name, "卡号", "奖金卡")].isna())]
        if not res.empty:
            res = export_columns(res)
            val_dict['缺少奖金卡信息'] = res.copy()
    return val_dict


def validator_tax_info(df):
    val_dict = {}
    if "个税调整_值" in df.columns:
        res = df[(df["个税调整_值"].isna()) | (df["个税调整_值"].round(2) != 0)]
        # res = df
        if not res.empty:
            res = export_columns(
                res, ['证件号码', utils.suodeshui_column_name, '累计应补(退)税额', '个税调整_值'])
            val_dict['个税错误信息'] = res.copy()
    return val_dict


def validator_id_info(df):
    val_dict = {}
    if get_column_name(SalaryPersons.name, utils.person_id_column_name) in df.columns and utils.yingfa_column_name in df.columns:
        res = df[(df[utils.yingfa_column_name] > 0) & (
            df[get_column_name(SalaryPersons.name, utils.person_id_column_name)].isna())]
        if not res.empty:
            res = export_columns(res)
            val_dict['身份证错误信息'] = res.copy()
    return val_dict


def validator_gjj(df):
    val_dict = {}
    if get_column_name(SalaryGjj.name, "公积金方案") in df.columns:
        res = df[df[utils.gjj_v_column_name] == 'ERR']
        if not res.empty:
            res = export_columns(res)
            val_dict['公积金方案设置错误'] = res.copy()
    return val_dict


def validator_other(df):
    val_dict = {}
    if get_column_name(SalaryGzs.name, "薪酬模式") in df.columns and get_column_name(SalaryGzs.name, "岗位工资") in df.columns:
        # 缺少岗位工资
        res = df[(df[get_column_name(SalaryGzs.name, "薪酬模式")] ==
                  '岗位绩效工资制') & (df[get_column_name(SalaryGzs.name, "岗位工资")] == 0)]
        if not res.empty:
            res = export_columns(res)
            val_dict['岗位工资错误信息'] = res.copy()
        # 离岗休息实发未0验证
        res = df[(df[get_column_name(SalaryGzs.name, "薪酬模式")] ==
                  '生活费（2021年离岗休息）') & (df[get_column_name(SalaryGzs.name, "生活补贴")] == 0) & (df[get_column_name(SalaryGzs.name, "实发")] != 0)]
        if not res.empty:
            res = export_columns(res)
            val_dict['自主创业错误信息'] = res.copy()
         # 只管领导验证，防止跨年年功工资计算出值
        res = df[(df[get_column_name(SalaryGzs.name, "薪酬模式")] ==
                  '总部直管领导年薪制') & ((df[get_column_name(SalaryGzs.name, "工龄工资")].notna()) | (df[get_column_name(SalaryGzs.name, "岗位工资")].notna()))]
        if not res.empty:
            res = export_columns(res)
            val_dict['经营层薪酬错误信息'] = res.copy()
    return val_dict


def validator(df):
    """
    验证本期数据
    """
    val_dict = {}
    # writer = pd.ExcelWriter('效验结果.xlsx')
    # 银行卡
    bank_v = validator_bank_info(df)
    if len(bank_v) > 0:
        val_dict = {**val_dict, **bank_v}
    # 实发小于0
    sf_v = validator_sf_info(df)
    if len(sf_v) > 0:
        val_dict = {**val_dict, **sf_v}
    # 所得税核对
    tax_v = validator_tax_info(df)
    if len(tax_v) > 0:
        val_dict = {**val_dict, **tax_v}
    # 缺少身份证信息
    id_v = validator_id_info(df)
    if len(id_v) > 0:
        val_dict = {**val_dict, **id_v}
    # 公积金方案设置错误
    gjj_v = validator_gjj(df)
    if len(gjj_v) > 0:
        val_dict = {**val_dict, **gjj_v}
    # 其他信息
    other_v = validator_other(df)
    if len(other_v) > 0:
        val_dict = {**val_dict, **other_v}
    return val_dict


def export_columns(df, other=[]):
    # 编码 姓名
    columns = [utils.tax_column_name, utils.code_info_column_name, get_column_name(
        SalaryGzs.name, utils.name_info_column_name), utils.depart_display_column_name, get_column_name(SalaryGzs.name, utils.depart_info_column_name)]
    if len(other) != 0:
        columns.extend(other)
    return df[columns]


def get_export_path(period,  paths=[]):
    ps = [period, '系统导出']
    ps.extend(paths)
    path = utils.join_path(ps)
    return path


def export_all_errs(period, errs):
    file_dir = get_export_path(period, [utils.err_folder_name, '汇总数据'])
    file_name = f"{period}_效验结果.xlsx"
    utils.make_folder_if_nessage(file_dir)
    writer = pd.ExcelWriter(utils.file_path(file_dir, file_name))
    for name, df in errs.items():
        df.to_excel(writer, name)
    writer.save()


def export_errs_by_depart_type(period, errs, departs, depart_type=utils.depart_display_column_name):
    for depart in departs:
        file_dir = get_export_path(period, [utils.err_folder_name, depart])
        file_name = f"{period}_{depart}_效验结果.xlsx"

        depart_err = split_by_depart_type(errs, depart, depart_type)
        if len(depart_err) > 0:
            utils.make_folder_if_nessage(file_dir)
            writer = pd.ExcelWriter(utils.file_path(file_dir, file_name))
            for name, df in depart_err.items():
                df.to_excel(writer, name)
            writer.save()


def split_by_depart_type(errs, depart, depart_type=utils.depart_display_column_name):
    res = {}
    for name, df in errs.items():
        depart_df = df[df[depart_type] == depart]
        if not depart_df.empty:
            res[name] = depart_df
    return res


def merge_gz_and_jj(gz_infos, jj_infos):

    if not gz_infos.df.empty and not jj_infos.df.empty:
        df = pd.merge(gz_infos.df, jj_infos.df, on=[
            utils.code_info_column_name, utils.tax_column_name, utils.depart_display_column_name], how='outer', suffixes=['_工资', '_奖金'], copy=True)

    elif not gz_infos.df.empty and jj_infos.df.empty:
        df = gz_infos.df
    elif gz_infos.df.empty and not jj_infos.df.empty:
        df = jj_infos.df
    append_yingf_shif_shui(df)
    return df


def append_yingf_shif_shui(df):
    if get_column_name(SalaryGzs.name, "应发") in df.columns and get_column_name(SalaryJjs.name, "应发") in df.columns:
        df[utils.yingfa_column_name] = df[get_column_name(
            SalaryGzs.name, "应发")].add(df[get_column_name(SalaryJjs.name, "应发")], fill_value=0)
    elif get_column_name(SalaryGzs.name, "应发") in df.columns and not get_column_name(SalaryJjs.name, "应发") in df.columns:
        df[utils.yingfa_column_name] = df[get_column_name(
            SalaryGzs.name, "应发")]
    elif not get_column_name(SalaryGzs.name, "应发") in df.columns and get_column_name(SalaryJjs.name, "应发") in df.columns:
        df[utils.yingfa_column_name] = df[get_column_name(
            SalaryJjs.name, "应发")]
    else:
        df[utils.yingfa_column_name] = pd.NA

    if get_column_name(SalaryGzs.name, "实发") in df.columns and get_column_name(SalaryJjs.name, "实发") in df.columns:
        df[utils.shifa_column_name] = df[get_column_name(
            SalaryGzs.name, "实发")].add(df[get_column_name(SalaryJjs.name, "实发")], fill_value=0)
    elif get_column_name(SalaryGzs.name, "实发") in df.columns and not get_column_name(SalaryJjs.name, "实发") in df.columns:
        df[utils.shifa_column_name] = df[get_column_name(
            SalaryGzs.name, "实发")]
    elif not get_column_name(SalaryGzs.name, "实发") in df.columns and get_column_name(SalaryJjs.name, "实发") in df.columns:
        df[utils.shifa_column_name] = df[get_column_name(
            SalaryJjs.name, "实发")]
    else:
        df[utils.shifa_column_name] = pd.NA

    if get_column_name(SalaryJjs.name, "个调税") in df.columns and get_column_name(SalaryGzs.name, "个调税") in df.columns:
        if get_column_name(SalaryJjs.name, "个税调整") in df.columns:
            df[utils.suodeshui_column_name_o] = (df.loc[:, [get_column_name(
                SalaryGzs.name, "个调税"), get_column_name(SalaryJjs.name, "个调税"), get_column_name(SalaryJjs.name, "个税调整")]].sum(axis=1))
        else:
            df[utils.suodeshui_column_name_o] = (df.loc[:, [get_column_name(
                SalaryGzs.name, "个调税"), get_column_name(SalaryJjs.name, "个调税")]].sum(axis=1))
        df[utils.suodeshui_column_name_o] = df[utils.suodeshui_column_name_o].apply(
            gts)
    if get_column_name(SalaryJjs.name, "应扣缴税额_正常工资薪金") in df.columns and get_column_name(SalaryGzs.name, "应扣缴税额_正常工资薪金") in df.columns:
        df.fillna({get_column_name(SalaryJjs.name, "应扣缴税额_正常工资薪金"): 0,
                   get_column_name(SalaryGzs.name, "应扣缴税额_正常工资薪金"): 0}, inplace=True)
        df[utils.suodeshui_column_name] = df[get_column_name(SalaryGzs.name, "应扣缴税额_正常工资薪金")].add(
            df[get_column_name(SalaryJjs.name, "应扣缴税额_正常工资薪金")], fill_value=0)
    elif not get_column_name(SalaryJjs.name, "应扣缴税额_正常工资薪金") in df.columns and get_column_name(SalaryGzs.name, "应扣缴税额_正常工资薪金") in df.columns:
        df[utils.suodeshui_column_name] = df[get_column_name(
            SalaryGzs.name, "应扣缴税额_正常工资薪金")]
    elif get_column_name(SalaryJjs.name, "应扣缴税额_正常工资薪金") in df.columns and not get_column_name(SalaryGzs.name, "应扣缴税额_正常工资薪金") in df.columns:
        df[utils.suodeshui_column_name] = df[get_column_name(
            SalaryJjs.name, "应扣缴税额_正常工资薪金")]
    else:
        df[utils.suodeshui_column_name] = pd.NA
    if get_column_name(SalaryJjs.name, "应纳税额_全年一次性奖金") in df.columns:
        df.fillna(
            {get_column_name(SalaryJjs.name, "应纳税额_全年一次性奖金"): 0}, inplace=True)
        df[utils.suodeshui_column_name] += df[get_column_name(
            SalaryJjs.name, "应纳税额_全年一次性奖金")]

    if utils.suodeshui_column_name_o in df.columns:
        df[utils.suodeshui_column_name] = df[utils.suodeshui_column_name].add(
            df[utils.suodeshui_column_name_o], fill_value=0)
    if get_column_name(SalaryGzs.name, '兼课带教费') in df.columns and get_column_name(SalaryGzs.name, '驻外津贴') in df.columns:
        df[utils.shouru_column_name] = (df.loc[:, [utils.yingfa_column_name, get_column_name(
            SalaryGzs.name, "兼课带教费"), get_column_name(SalaryGzs.name, "驻外津贴")]].sum(axis=1))
    else:
        if get_column_name(SalaryGzs.name, '驻外津贴') in df.columns:
            df[utils.shouru_column_name] = df[utils.yingfa_column_name].add(
                df[get_column_name(SalaryGzs.name, '驻外津贴')], fill_value=0)
        if get_column_name(SalaryGzs.name, '兼课带教费') in df.columns:
            df[utils.shouru_column_name] = df[utils.yingfa_column_name].add(
                df[get_column_name(SalaryGzs.name, '兼课带教费')], fill_value=0)
    # df[utils.shouru_column_name] = df[utils.yingfa_column_name]
    if get_column_name(SalaryJjs.name, '年底兑现奖') in df.columns:
        df[utils.shouru_column_name] = df[utils.shouru_column_name].sub(
            df[get_column_name(SalaryJjs.name, '年底兑现奖')], fill_value=0)

    if get_column_name(SalaryGzs.name, utils.depart_info_column_name) in df.columns and get_column_name(SalaryJjs.name, utils.depart_info_column_name) in df.columns:
        df.loc[df[get_column_name(SalaryGzs.name, utils.depart_info_column_name)].isnull(), get_column_name(SalaryGzs.name, utils.depart_info_column_name)
               ] = df[df[get_column_name(SalaryGzs.name, utils.depart_info_column_name)].isnull()][get_column_name(SalaryJjs.name, utils.depart_info_column_name)]
    if get_column_name(SalaryGzs.name, utils.name_info_column_name) in df.columns and get_column_name(SalaryJjs.name, utils.depart_info_column_name) in df.columns:
        df.loc[df[get_column_name(SalaryGzs.name, utils.name_info_column_name)].isnull(), get_column_name(SalaryGzs.name, utils.name_info_column_name)] = df[df[get_column_name(
            SalaryGzs.name, utils.name_info_column_name)].isnull()][get_column_name(SalaryJjs.name, utils.name_info_column_name)]
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
    return pd.merge(df, id_df, on=[utils.code_info_column_name], how='left')


def contact_bank_info(df, banks):
    if banks.df.empty:
        return df
    if not banks.df.empty:
        bank_df = banks.df[[utils.code_info_column_name,  utils.tax_column_name, get_column_name(
            banks.name, "金融机构", "工资卡"), get_column_name(
            banks.name, "卡号", "工资卡"), get_column_name(
            banks.name, "金融机构", "奖金卡"), get_column_name(
            banks.name, "卡号", "奖金卡")]]
        return pd.merge(df, bank_df, on=[
            utils.code_info_column_name, utils.tax_column_name], how='left')


def contact_job_info(df, jobs):
    if not jobs.df.empty:
        job_df = jobs.df[[utils.code_info_column_name,  utils.tax_column_name, utils.depart_display_column_name, get_column_name(
            jobs.name, "岗位类型"), get_column_name(
            jobs.name, "执行岗位名称"), get_column_name(
            jobs.name, "岗位层级"), get_column_name(
            jobs.name, "组合(岗位序列+标准目录+岗位层级)")]]
        return pd.merge(df, job_df, on=[
            utils.code_info_column_name, utils.tax_column_name, utils.depart_display_column_name], how='left')
    else:
        return df


def contact_tax_info(df, tax):
    if not tax.df.empty:
        tax_df = tax.df[[utils.person_id_column_name,
                         utils.tax_column_name, "累计应补(退)税额"]]
        df.loc[:, f'人员信息导出结果-证件号码_lower'] = df['人员信息导出结果-证件号码'].str.lower()
        tax_df.loc[:, f'{utils.person_id_column_name}_lower'] = tax_df[utils.person_id_column_name].str.lower()
        return pd.merge(df, tax_df, left_on=["人员信息导出结果-证件号码_lower", utils.tax_column_name], right_on=[
            f'{utils.person_id_column_name}_lower', utils.tax_column_name], how='outer')
    else:
        return df


def contact_tax_one_info(df, taxone):
    if not taxone.df.empty:
        tax_df = taxone.df[[utils.person_id_column_name,
                            utils.tax_column_name, "累计应补(退)税额"]]
        tax_df.rename(columns={'累计应补(退)税额': '累计应补(退)税额_一次性'}, inplace=True)
        tax_df.loc[:, f'{utils.person_id_column_name}_一次性_lower'] = tax_df[utils.person_id_column_name].str.lower()
        return pd.merge(df, tax_df[[f'{utils.person_id_column_name}_一次性_lower',
                                    utils.tax_column_name, "累计应补(退)税额_一次性"]], left_on=["人员信息导出结果-证件号码_lower", utils.tax_column_name], right_on=[
            f'{utils.person_id_column_name}_一次性_lower', utils.tax_column_name], how='outer')
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
    sap_df["实发核对"] = pd.NA
    depart_df = df[get_column_name(
        SalaryGzs.name, utils.depart_info_column_name)].str.split(r"\\", expand=True)
    sap_df["一级机构"] = depart_df[0]
    sap_df["二级机构"] = depart_df[1]
    sap_df["三级机构"] = depart_df[2]
    sap_df["四级机构"] = depart_df[3]
    sap_df["五级机构"] = depart_df[4]
    sap_df["员工编号"] = get_df_values(df, utils.code_info_column_name)
    sap_df["员工姓名"] = get_df_values(df, get_column_name(SalaryGzs.name, "员工姓名"))
    sap_df["身份证"] = get_df_values(df, utils.person_id_column_name)
    sap_df["工资范围"] = get_df_values(df, utils.depart_display_column_name)
    sap_df["人事范围"] = depart_df[1]
    sap_df["员工组"] = get_df_values(
        df, get_column_name(SalaryPersons.name, "人员类型"))
    sap_df["员工子组"] = get_df_values(
        df, get_column_name(SalaryPersons.name, "在职状态"))
    # sap_df["职位"] = get_df_values(df, get_column_name(
    #     SalaryPersonJobs.name, "组合(岗位序列+标准目录+岗位层级)"))
    # sap_df["职族"] = get_df_values(df, get_column_name(
    #     SalaryPersonJobs.name, "岗位类型"))
    sap_df["职位"] = get_df_values(df, get_column_name(
        SalaryPersons.name, "岗位"))
    sap_df["职族"] = get_df_values(df, get_column_name(
        SalaryPersons.name, "标准岗位层级"))
    sap_df["岗位工资"] = get_df_values(df, get_column_name(SalaryGzs.name, "岗位工资"))
    sap_df["保留工资"] = get_df_values(df, get_column_name(SalaryGzs.name, "保留工资"))
    sap_df["年功工资"] = get_df_values(df, get_column_name(SalaryGzs.name, "工龄工资"))
    sap_df["辅助工资"] = get_df_values(
        df, get_column_name(SalaryGzs.name, "其他保留工资"))
    sap_df["生活补助"] = get_df_values(df, get_column_name(SalaryGzs.name, "生活补贴"))
    sap_df["考核工资"] = get_df_values(df, get_column_name(SalaryGzs.name, "考核浮动"))
    sap_df["工资补退"] = get_df_values(df, get_column_name(SalaryGzs.name, "工资调整"))
    sap_df["其他工资"] = get_df_values(df, get_column_name(SalaryGzs.name, "生活费"))
    sap_df["内退基本工资"] = get_df_values(
        df, get_column_name(SalaryGzs.name, "固定工资"))
    sap_df["内退增资"] = get_df_values(
        df, get_column_name(SalaryGzs.name, "待退休工资"))
    # 并入年功工资 通过薪酬模式区分
    sap_df["内退工龄工资"] = pd.NA
    sap_df["代缴三金"] = get_df_values(
        df, get_column_name(SalaryGzs.name, "生活费补差"))
    sap_df["物价补贴"] = get_df_values(
        df, get_column_name(SalaryGzs.name, "水电气暖物业补贴"))
    sap_df["夜班津贴"] = get_df_values(
        df, get_column_name(SalaryGzs.name, "中夜班津贴"))
    sap_df["技师津贴"] = get_df_values(df, get_column_name(SalaryGzs.name, "技能津贴"))
    sap_df["一专多能工津贴"] = get_df_values(
        df, get_column_name(SalaryGzs.name, "兼岗工资"))
    sap_df["矿山津贴"] = pd.NA
    sap_df["下井津贴"] = pd.NA
    sap_df["教、护龄津贴"] = get_df_values(
        df, get_column_name(SalaryGzs.name, "驻外津贴"))
    sap_df["护士长津贴"] = pd.NA
    sap_df["外语津贴"] = get_df_values(df, get_column_name(SalaryGzs.name, "学历津贴"))
    sap_df["班组长津贴"] = get_df_values(
        df, get_column_name(SalaryGzs.name, "班组长津贴"))
    sap_df["科技津贴"] = get_df_values(
        df, get_column_name(SalaryGzs.name, "科技优秀津贴"))
    sap_df["能手津贴"] = get_df_values(
        df, get_column_name(SalaryGzs.name, "操作能手津贴"))
    sap_df["基本奖金"] = get_df_values(df, get_column_name(SalaryJjs.name, "基本奖金"))
    sap_df["单项奖1"] = get_df_values(df, get_column_name(SalaryJjs.name, "单项奖1"))
    sap_df["单项奖2"] = get_df_values(df, get_column_name(SalaryJjs.name, "单项奖2"))
    sap_df["单项奖3"] = get_df_values(df, get_column_name(SalaryJjs.name, "单项奖3"))
    sap_df["法定节日加班工资"] = get_df_values(
        df, get_column_name(SalaryGzs.name, "法定假日加班工资"))
    sap_df["公休日加班工资"] = get_df_values(
        df, get_column_name(SalaryGzs.name, "休息日加班工资"))
    sap_df["平时加班工资"] = get_df_values(
        df, get_column_name(SalaryGzs.name, "平常加班工资"))
    sap_df["缺勤扣款合计"] = get_df_values(
        df, get_column_name(SalaryGzs.name, "缺勤扣款单元"))
    sap_df["公积金"] = get_df_values(
        df, get_column_name(SalaryGzs.name, "公积金个人额度"))
    sap_df["养老保险"] = get_df_values(
        df, get_column_name(SalaryGzs.name, "养老保险个人额度"))
    sap_df["医疗保险缴"] = get_df_values(
        df, get_column_name(SalaryGzs.name, "医疗保险个人额度"))
    sap_df["失业保险"] = get_df_values(
        df, get_column_name(SalaryGzs.name, "失业保险个人额度"))
    sap_df["养老保险补缴"] = pd.NA
    sap_df["医疗保险补缴"] = pd.NA
    sap_df["失业保险补缴"] = pd.NA
    sap_df["年金"] = get_df_values(
        df, get_column_name(SalaryGzs.name, "企业年金个人基础缴费"))
    sap_df["工资税收"] = get_df_values(df, get_column_name(SalaryGzs.name, "所得税"))
    sap_df["水利基金"] = get_df_values(
        df, get_column_name(SalaryGzs.name, "其他代扣款"))
    sap_df["财务扣款"] = get_df_values(df, get_column_name(SalaryGzs.name, "其他扣款"))
    sap_df["电费"] = pd.NA
    sap_df["房租"] = pd.NA
    sap_df["收视费"] = pd.NA
    sap_df["清洁费"] = pd.NA
    sap_df["乘车费用"] = pd.NA
    sap_df["财务补退"] = get_df_values(df, get_column_name(
        SalaryJjs.name, "其它补发")) + get_df_values(df, get_column_name(SalaryGzs.name, "补发一"))
    sap_df["物业补贴"] = get_df_values(
        df, get_column_name(SalaryGzs.name, "水电气暖物业补贴"))
    sap_df["保健费"] = get_df_values(df, get_column_name(SalaryGzs.name, "出勤津贴"))
    sap_df["独补"] = get_df_values(df, get_column_name(SalaryGzs.name, "独生子女费"))
    sap_df["通讯费"] = get_df_values(df, get_column_name(SalaryGzs.name, "通讯补贴"))
    sap_df["防暑降温"] = get_df_values(df, get_column_name(SalaryGzs.name, "高温津贴"))
    sap_df["回民"] = get_df_values(df, get_column_name(SalaryGzs.name, "民族津贴"))
    sap_df["纪检津贴"] = pd.NA
    sap_df["计生津贴"] = pd.NA
    sap_df["误餐补贴"] = get_df_values(df, get_column_name(SalaryGzs.name, "误餐补助"))
    sap_df["矿山荣誉金"] = pd.NA
    sap_df["信访津贴"] = pd.NA
    sap_df["伤残津贴"] = get_df_values(df, get_column_name(SalaryGzs.name, "工伤津贴"))
    sap_df["职务补贴"] = get_df_values(df, get_column_name(SalaryGzs.name, "公务车贴"))
    sap_df["科研项目津贴"] = get_df_values(
        df, get_column_name(SalaryGzs.name, "特殊贡献津贴"))
    sap_df["技术攻关津贴"] = get_df_values(
        df, get_column_name(SalaryGzs.name, "技术津贴"))
    sap_df["非工资性津贴补发"] = get_df_values(
        df, get_column_name(SalaryGzs.name, "各项补贴"))
    sap_df["工资应发"] = get_df_values(df, utils.yingfa_column_name)
    sap_df["实发工资"] = get_df_values(df, utils.shifa_column_name)
    sap_df["教育经费"] = get_df_values(
        df, get_column_name(SalaryGzs.name, "兼课带教费"))
    sap_df["工程津贴"] = get_df_values(
        df, get_column_name(SalaryJjs.name, "工程津贴"))
    sap_df["技术输出"] = get_df_values(
        df, get_column_name(SalaryJjs.name, "技术输出"))
    sap_df["其他"] = get_df_values(
        df, get_column_name(SalaryJjs.name, "争取国家政策奖"))
    sap_df["公司效益奖"] = get_df_values(
        df, get_column_name(SalaryJjs.name, "公司效益奖"))
    sap_df["上卡效益奖"] = pd.NA
    sap_df["效益奖所得税"] = pd.NA
    sap_df["年底兑现奖"] = get_df_values(
        df, get_column_name(SalaryJjs.name, "年底兑现奖"))
    sap_df["年终奖实发"] = pd.NA
    sap_df["年终奖所得税"] = pd.NA
    sap_df["计税奖金"] = get_df_values(
        df, get_column_name(SalaryJjs.name, "计税奖金"))
    sap_df["预支年薪"] = get_df_values(
        df, get_column_name(SalaryGzs.name, "月固定薪资"))+get_df_values(
        df, get_column_name(SalaryGzs.name, "绩效工资"))+get_df_values(
        df, get_column_name(SalaryGzs.name, "预发绩效年薪"))
    sap_df["执业工资"] = pd.NA

    sap_df["上卡工资"] = get_df_values(
        df, get_column_name(SalaryGzs.name, "实发"))
    sap_df["上卡年终奖"] = pd.NA
    sap_df["上卡基本奖"] = get_df_values(
        df, get_column_name(SalaryJjs.name, "实发"))
    sap_df["银行卡1"] = get_df_values(
        df, get_column_name(SalaryBanks.name, "卡号", "工资卡"))
    sap_df["银行1"] = get_df_values(
        df, get_column_name(SalaryBanks.name, "金融机构", "工资卡"))
    sap_df["银行卡2"] = get_df_values(
        df, get_column_name(SalaryBanks.name, "卡号", "奖金卡"))
    sap_df["银行2"] = get_df_values(
        df, get_column_name(SalaryBanks.name, "金融机构", "奖金卡"))
    sap_df["子女教育"] = get_df_values(
        df, get_column_name(SalaryGzs.name, "累计子女教育支出"))
    sap_df["继续教育"] = get_df_values(
        df, get_column_name(SalaryGzs.name, "累计继续教育支出"))
    sap_df["住房贷款利息"] = get_df_values(
        df, get_column_name(SalaryGzs.name, "累计住房贷款利息支出"))
    sap_df["住房租金"] = get_df_values(
        df, get_column_name(SalaryGzs.name, "累计住房租金支出"))
    sap_df["赡养老人"] = get_df_values(
        df, get_column_name(SalaryGzs.name, "累计赡养老人支出"))
    sap_df["马钢工龄"] = pd.NA
    sap_df["工龄"] = get_df_values(
        df, get_column_name(SalaryPersons.name, "参加工作时间"))
    sap_df["财务代发计税项"] = get_df_values(
        df, get_column_name(SalaryGzs.name, "其它纳税收入"))
    sap_df["财务代发非计税项"] = pd.NA
    sap_df["累计应发"] = pd.NA
    sap_df["累计五险两金"] = pd.NA
    sap_df["累计其他计税"] = pd.NA
    sap_df["累计标准免税额"] = pd.NA
    sap_df["累计个税"] = pd.NA
    sap_df["司法扣款"] = get_df_values(
        df, get_column_name(SalaryGzs.name, "司法扣款"))
    sap_df["重点工作专项奖"] = get_df_values(
        df, get_column_name(SalaryJjs.name, "重点工作专项奖"))
    sap_df["荣誉类奖"] = get_df_values(
        df, get_column_name(SalaryJjs.name, "荣誉类奖"))
    sap_df["员工精益改善奖"] = get_df_values(
        df, get_column_name(SalaryJjs.name, "员工精益改善奖"))
    sap_df["宝武集团单列奖励"] = get_df_values(
        df, get_column_name(SalaryJjs.name, "宝武集团单列奖励"))
    sap_df["劳动竞赛奖"] = get_df_values(
        df, get_column_name(SalaryJjs.name, "劳动竞赛奖"))
    sap_df["安全绩效奖"] = get_df_values(
        df, get_column_name(SalaryJjs.name, "安全绩效奖"))
    sap_df["考核扣减"] = get_df_values(
        df, get_column_name(SalaryJjs.name, "考核扣减"))
    sap_df["绩效薪预支"] = get_df_values(
        df, get_column_name(SalaryJjs.name, "绩效薪预支"))
    sap_df["绩效薪结算"] = get_df_values(
        df, get_column_name(SalaryJjs.name, "绩效薪结算"))
    sap_df["科技奖励"] = get_df_values(
        df, get_column_name(SalaryJjs.name, "科技奖励"))
    sap_df["外派人员履职待遇"] = get_df_values(
        df, get_column_name(SalaryJjs.name, "外派人员履职待遇"))
    sap_df[utils.tax_column_name] = get_df_values(df, utils.tax_column_name)
    sap_df[utils.depart_display_column_name] = get_df_values(
        df, utils.depart_display_column_name)
    # 护士长津贴	外语津贴	班组长津贴	科技津贴	能手津贴	基本奖金	单项奖1	单项奖2	单项奖3	法定节日加班工资	公休日加班工资	平时加班工资
    # 缺勤扣款合计	公积金	养老保险	医疗保险缴	失业保险
    # 养老保险补缴	医疗保险补缴	失业保险补缴	年金	工资税收	水利基金	财务扣款
    # 电费	房租	收视费	清洁费	乘车费用	财务补退	物业补贴	保健费	独补	通讯费
    # 防暑降温	回民	纪检津贴	计生津贴	误餐补贴	矿山荣誉金	信访津贴	伤残津贴
    # 职务补贴	科研项目津贴	技术攻关津贴	非工资性津贴补发	工资应发	实发工资
# 教育经费	工程津贴	技术输出	其他	公司效益奖	上卡效益奖	效益奖所得税	年底兑现奖	年终奖实发	年终奖所得税	计税奖金	预支年薪	执业工资	上卡工资	上卡年终奖	上卡基本奖
# 银行卡1	银行1	银行卡2	银行2	子女教育	继续教育	住房贷款利息	住房租金	赡养老人	马钢工龄	工龄	财务代发计税项	财务代发非计税项	累计应发	累计五险两金	累计其他计税	累计标准免税额	累计个税
# 司法扣款	重点工作专项奖	荣誉类奖	员工精益改善奖	宝武集团单列奖励	劳动竞赛奖	安全绩效奖
# 考核扣减	绩效薪预支	绩效薪结算	科技奖励	外派人员履职待遇
    return sap_df


def get_df_values(df, name):
    v = pd.NA
    if name in df.columns:
        v = df[name]
    return v
