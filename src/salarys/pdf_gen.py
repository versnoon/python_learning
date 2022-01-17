#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   pdf_gen.py
@Time    :   2021/07/03 11:50:48
@Author  :   Tong tan
@Version :   1.0
@Contact :   tongtan@gmail.com
'''

from os.path import join
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm

from PyPDF4 import PdfFileWriter, PdfFileReader


from src.salarys import utils


file_path_prefix = utils.root_dir_()
period = ''
filename_suffix = '工资费用资金调拨单'


class SalaryPay:

    def __init__(self) -> None:
        self.period = ''
        self.depart = ''
        self.sealname = ''
        self._total_sf = 0
        self._yangl_gr = 0
        self._yangl_qy = 0

        self._yil_gr = 0
        self._yil_qy = 0

        self._sy_gr = 0
        self._sy_qy = 0

        self._gjj_gr = 0
        self._gjj_qy = 0

        self._nj_gr = 0
        self._nj_qy = 0

        self._gs = 0  # 工伤
        self._sy = 0  # 生育

        self._total_bank_gh_sf = 0  # 工行实发
        self._total_bank_zh_sf = 0  # 中行实发
        self._total_bank_jh_sf = 0  # 建行实发

        self._total_gjj_jh = 0  # 建行公积金
        self._total_gjj_gh = 0  # 工行公积金

    @property
    def total_sf(self):
        return round(self._total_sf, 2)

    @property
    def yangl_gr(self):
        return round(self._yangl_gr, 2)

    @property
    def yangl_qy(self):
        return round(self._yangl_qy, 2)

    @property
    def yil_gr(self):
        return round(self._yil_gr, 2)

    @property
    def yil_qy(self):
        return round(self._yil_qy, 2)

    @property
    def sy_gr(self):
        return round(self._sy_gr, 2)

    @property
    def sy_qy(self):
        return round(self._sy_qy, 2)

    @property
    def gjj_gr(self):
        return round(self._gjj_gr, 2)

    @property
    def gjj_qy(self):
        return round(self._gjj_qy, 2)

    @property
    def nj_gr(self):
        return round(self._nj_gr, 2)

    @property
    def nj_qy(self):
        return round(self._nj_qy, 2)

    @property
    def gs(self):
        return round(self._gs, 2)

    @property
    def sy(self):
        return round(self._sy, 2)

    @property
    def total_bank_gh_sf(self):
        return round(self._total_bank_gh_sf, 2)

    @property
    def total_bank_zh_sf(self):
        return round(self._total_bank_zh_sf, 2)

    @property
    def total_bank_jh_sf(self):
        return round(self._total_bank_jh_sf, 2)

    @property
    def total_gjj_jh(self):
        return round(self._total_gjj_jh, 2)

    @property
    def total_gjj_gh(self):
        return round(self._total_gjj_gh, 2)

    def yangl_total(self):
        return round(self._yangl_gr + self._yangl_qy, 2)

    def yil_total(self):
        return round(self._yil_gr + self._yil_qy, 2)

    def sy_total(self):
        return round(self._sy_gr + self._sy_qy, 2)

    def bx_total(self):
        return round(self.yangl_total() + self.yil_total() + self.sy_total() + self._sy + self._gs, 2)

    def gjj_total(self):
        return round(self._gjj_gr + self._gjj_qy, 2)

    def nj_total(self):
        return round(self._nj_gr + self._nj_qy, 2)

    def total(self):
        return round(self.bx_total() + self.gjj_total() + self.nj_total() + self._total_sf, 2)

    # def to_salary_pay_group_by_depart(self, period, depart, sealname, merges, departs):
    #     salary_pay = SalaryPay()
    #     salary_pay.period = period
    #     salary_pay.depart = depart
    #     salary_pay.sealname = sealname
    #     gjj_type = self.get_gjj_type(depart, departs)
    #     for d in merges.values():
    #         p_info = d[0]
    #         if len(d) > 0 and d[0]:
    #             p_info: PersonSalaryInfo = d[0]
    #             gz = p_info._gz
    #             jj = p_info._jj
    #             banks = p_info._banks
    #             self.add_payinfo(salary_pay, gz, jj, banks, gjj_type)

    #     return salary_pay

    # def to_salary_pay_group_by_tex_depart(self, period, tex_depart, sealname, merges, departs):
    #     salary_pay = SalaryPay()
    #     salary_pay.period = period
    #     salary_pay.depart = tex_depart
    #     salary_pay.sealname = sealname
    #     for depart, datas_by_depart in merges.items():
    #         gjj_type = self.get_gjj_type(depart, departs)
    #         for d in datas_by_depart.values():
    #             p_info = d[0]
    #             if len(d) > 0 and d[0]:
    #                 p_info: PersonSalaryInfo = d[0]
    #                 gz = p_info._gz
    #                 jj = p_info._jj
    #                 banks = p_info._banks
    #                 self.add_payinfo(salary_pay, gz, jj, banks, gjj_type)
    #     return salary_pay

    def get_gjj_type(self, depart, departs):
        for d in departs.values():
            if d.get_depart_salaryScope_and_name() == depart:
                return d.gjjType
        return ""

    # def add_payinfo(self, salary_pay, gz, jj, banks, gjj_type):
    #     '''完成金额汇总
    #     '''

    #     if gz:
    #         # 汇总
    #         # 实发
    #         salary_pay._total_sf += gz._pay
    #         # 保险
    #         salary_pay._yangl_gr += 0-gz._yl_bx
    #         salary_pay._yangl_qy += 0-gz._yl_qybx

    #         salary_pay._yil_gr += 0-gz._yil_bx
    #         salary_pay._yil_qy += 0-gz._yil_qybx

    #         salary_pay._sy_gr += 0-gz._sy_bx
    #         salary_pay._sy_qy += 0-gz._sy_qybx

    #         salary_pay._gs += 0-gz._gs_qybx
    #         salary_pay._sy += 0-gz._shy_qybx

    #         # 公积金年金
    #         salary_pay._gjj_gr += 0-gz._gjj_bx
    #         salary_pay._gjj_qy += 0-gz._gjj_qybx

    #         salary_pay._nj_gr += 0-gz._nj_bx
    #         salary_pay._nj_qy += 0-gz._nj_qybx

    #         # 公积金
    #         if "马鞍山公积金中心" == gjj_type:
    #             salary_pay._total_gjj_jh += 0-gz._gjj_bx + 0 - gz._gjj_qybx
    #         elif "马钢公积金中心-工行" == gjj_type:
    #             salary_pay._total_gjj_gh += 0-gz._gjj_bx + 0 - gz._gjj_qybx

    #     if jj:
    #         salary_pay._total_sf += jj._pay
    #     if banks:
    #         if 'gz' in banks:
    #             gz_bank = banks['gz']
    #             if '工商银行' in gz_bank._financialInstitution:
    #                 if gz:
    #                     salary_pay._total_bank_gh_sf += gz._pay
    #             if '中国银行' in gz_bank._financialInstitution:
    #                 if gz:
    #                     salary_pay._total_bank_zh_sf += gz._pay
    #             if '建设银行' in gz_bank._financialInstitution:
    #                 if gz:
    #                     salary_pay._total_bank_jh_sf += gz._pay
    #         if 'jj' in banks:
    #             jj_bank = banks['jj']
    #             if '工商银行' in jj_bank._financialInstitution:
    #                 if jj:
    #                     salary_pay._total_bank_gh_sf += jj._pay
    #             if '中国银行' in jj_bank._financialInstitution:
    #                 if jj:
    #                     salary_pay._total_bank_zh_sf += jj._pay
    #             if '建设银行' in jj_bank._financialInstitution:
    #                 if jj:
    #                     salary_pay._total_bank_jh_sf += jj._pay


def create_pdf_new(period, departs, df):
    for tex_depart in departs.tax_departs():
        salary_pay = to_salary_pay(period, tex_depart, df)
        to_tax_depart_new(period, file_name(
            period, tex_depart), tex_depart, salary_pay.sealname, salary_pay)
        for depart in departs.depart_dispaly_names():
            t = departs.is_in_tax_depart(tex_depart, depart)
            if t:
                salary_pay = to_salary_pay_depart(
                    period, tex_depart, df, depart)
                to_tax_depart_new(period, file_name(
                    period, depart), depart, salary_pay.sealname, salary_pay, False)


def to_salary_pay(period, tex_depart, df):
    salary_pay = SalaryPay()
    salary_pay.period = period
    salary_pay.sealname = seal_name(tex_depart)
    salary_pay.depart = tex_depart
    if df[utils.tax_column_name].str.contains(tex_depart).any():
        tg = df.groupby([utils.tax_column_name]).sum()
        salary_pay._total_sf = tg.loc[tex_depart, '实发合计']
        if '工资信息-养老保险个人额度' in df.columns:
            salary_pay._yangl_gr = tg.loc[tex_depart, '工资信息-养老保险个人额度']
            salary_pay._yangl_qy = tg.loc[tex_depart, '工资信息-养老保险企业额度']
            salary_pay._yil_gr = tg.loc[tex_depart, '工资信息-医疗保险个人额度']
            salary_pay._yil_qy = tg.loc[tex_depart, '工资信息-医疗保险企业额度']
            salary_pay._sy_gr = tg.loc[tex_depart, '工资信息-失业保险个人额度']
            salary_pay._sy_qy = tg.loc[tex_depart, '工资信息-失业保险企业额度']
            salary_pay._gjj_gr = tg.loc[tex_depart, '工资信息-公积金个人额度']
            salary_pay._gjj_qy = tg.loc[tex_depart, '工资信息-公积金企业额度']
            salary_pay._nj_gr = tg.loc[tex_depart, '工资信息-企业年金个人基础缴费']
            salary_pay._nj_qy = tg.loc[tex_depart, '工资信息-企业年金企业额度']
            salary_pay._gs = tg.loc[tex_depart, '工资信息-工伤保险企业额度']
            salary_pay._sy = tg.loc[tex_depart, '工资信息-生育保险企业额度']
        if '银行卡信息-金融机构_工资卡' in df.columns:
            tg = df.groupby([utils.tax_column_name, '银行卡信息-金融机构_工资卡']).sum()
            if '工资信息-实发' in df.columns:
                salary_pay._total_bank_gh_sf = tg.loc[(
                    tex_depart, '中国工商银行'), '工资信息-实发']
                salary_pay._total_bank_zh_sf = tg.loc[(
                    tex_depart, '中国银行'), '工资信息-实发']
                salary_pay._total_bank_jh_sf = tg.loc[(
                    tex_depart, '中国建设银行'), '工资信息-实发']
        if '银行卡信息-金融机构_奖金卡' in df.columns:
            tg = df.groupby([utils.tax_column_name, '银行卡信息-金融机构_奖金卡']).sum()
            if '奖金信息-实发' in df.columns:
                salary_pay._total_bank_gh_sf += tg.loc[(
                    tex_depart, '中国工商银行'), '奖金信息-实发']
                salary_pay._total_bank_zh_sf += tg.loc[(
                    tex_depart, '中国银行'), '奖金信息-实发']
                salary_pay._total_bank_jh_sf += tg.loc[(
                    tex_depart, '中国建设银行'), '奖金信息-实发']
        if '公积金信息-公积金方案' in df.columns:
            tg = df.groupby([utils.tax_column_name, '公积金信息-公积金方案']).sum()
            if '马鞍山钢铁股份有限公司（总部）' == tex_depart:
                if '工资信息-公积金个人额度' in df.columns and '工资信息-公积金企业额度' in df.columns:
                    salary_pay._total_gjj_gh = tg.loc[(tex_depart, '马鞍山钢铁股份有限公司（总部）公积金方案_1'), '工资信息-公积金个人额度'] + \
                        tg.loc[(tex_depart, '马鞍山钢铁股份有限公司（总部）公积金方案_1'),
                               '工资信息-公积金企业额度']
                    salary_pay._total_gjj_jh = tg.loc[(tex_depart, '马鞍山钢铁股份有限公司（总部）公积金方案_2'), '工资信息-公积金个人额度'] + \
                        tg.loc[(tex_depart, '马鞍山钢铁股份有限公司（总部）公积金方案_2'),
                               '工资信息-公积金企业额度']
    return salary_pay


def to_salary_pay_depart(period, tex_depart, df, depart):
    salary_pay = SalaryPay()
    salary_pay.period = period
    salary_pay.sealname = seal_name(tex_depart)
    salary_pay.depart = depart
    if df[utils.depart_display_column_name].str.contains(depart).any():
        tg = df.groupby(
            [utils.tax_column_name, utils.depart_display_column_name]).sum()
        tgx = df.groupby(
            [utils.tax_column_name, utils.depart_display_column_name, utils.depart_column_name, '银行卡信息-金融机构_工资卡']).sum()

        tgx = df.groupby(
            [utils.tax_column_name, utils.depart_display_column_name, utils.depart_column_name, '银行卡信息-金融机构_奖金卡']).sum()

        salary_pay._total_sf = tg.loc[(tex_depart, depart), '实发合计']
        if '工资信息-养老保险个人额度' in df.columns:
            salary_pay._yangl_gr = tg.loc[(
                tex_depart, depart), '工资信息-养老保险个人额度']
            salary_pay._yangl_qy = tg.loc[(
                tex_depart, depart), '工资信息-养老保险企业额度']
            salary_pay._yil_gr = tg.loc[(tex_depart, depart), '工资信息-医疗保险个人额度']
            salary_pay._yil_qy = tg.loc[(tex_depart, depart), '工资信息-医疗保险企业额度']
            salary_pay._sy_gr = tg.loc[(tex_depart, depart), '工资信息-失业保险个人额度']
            salary_pay._sy_qy = tg.loc[(tex_depart, depart), '工资信息-失业保险企业额度']
            salary_pay._gjj_gr = tg.loc[(tex_depart, depart), '工资信息-公积金个人额度']
            salary_pay._gjj_qy = tg.loc[(tex_depart, depart), '工资信息-公积金企业额度']
            salary_pay._nj_gr = tg.loc[(tex_depart, depart), '工资信息-企业年金个人基础缴费']
            salary_pay._nj_qy = tg.loc[(tex_depart, depart), '工资信息-企业年金企业额度']
            salary_pay._gs = tg.loc[(tex_depart, depart), '工资信息-工伤保险企业额度']
            salary_pay._sy = tg.loc[(tex_depart, depart), '工资信息-生育保险企业额度']
        if '银行卡信息-金融机构_工资卡' in df.columns:
            tg = df.groupby([utils.tax_column_name,
                             utils.depart_display_column_name, '银行卡信息-金融机构_工资卡']).sum()
            if '工资信息-实发' in df.columns:
                total_bank_gh_sf_df = tg.loc[(tg.index.get_level_values(
                    0).str.startswith(tex_depart)) & (tg.index.get_level_values(1).str.startswith(depart)) & (tg.index.get_level_values(2).str.startswith('中国工商银行'))]
                if not total_bank_gh_sf_df.empty:
                    salary_pay._total_bank_gh_sf = total_bank_gh_sf_df['工资信息-实发'].iloc[0]
                total_bank_zh_sf_df = tg.loc[(tg.index.get_level_values(
                    0).str.startswith(tex_depart)) & (tg.index.get_level_values(1).str.startswith(depart)) & (tg.index.get_level_values(2).str.startswith('中国银行'))]
                if not total_bank_zh_sf_df.empty:
                    salary_pay._total_bank_zh_sf = total_bank_zh_sf_df['工资信息-实发'].iloc[0]
                total_bank_jh_sf_df = tg.loc[(tg.index.get_level_values(
                    0).str.startswith(tex_depart)) & (tg.index.get_level_values(1).str.startswith(depart)) & (tg.index.get_level_values(2).str.startswith('中国建设银行'))]
                if not total_bank_jh_sf_df.empty:
                    salary_pay._total_bank_jh_sf = total_bank_jh_sf_df['工资信息-实发'].iloc[0]
        if '银行卡信息-金融机构_奖金卡' in df.columns:
            tg = df.groupby([utils.tax_column_name,
                             utils.depart_display_column_name, '银行卡信息-金融机构_奖金卡']).sum()

            if '奖金信息-实发' in df.columns:
                total_bank_gh_sf_df = tg.loc[(tg.index.get_level_values(
                    0).str.startswith(tex_depart)) & (tg.index.get_level_values(1).str.startswith(depart)) & (tg.index.get_level_values(2).str.startswith('中国工商银行'))]
                if not total_bank_gh_sf_df.empty:
                    salary_pay._total_bank_gh_sf += total_bank_gh_sf_df['奖金信息-实发'].iloc[0]
                total_bank_zh_sf_df = tg.loc[(tg.index.get_level_values(
                    0).str.startswith(tex_depart)) & (tg.index.get_level_values(1).str.startswith(depart)) & (tg.index.get_level_values(2).str.startswith('中国银行'))]
                if not total_bank_zh_sf_df.empty:
                    salary_pay._total_bank_zh_sf += total_bank_zh_sf_df['奖金信息-实发'].iloc[0]
                total_bank_jh_sf_df = tg.loc[(tg.index.get_level_values(
                    0).str.startswith(tex_depart)) & (tg.index.get_level_values(1).str.startswith(depart)) & (tg.index.get_level_values(2).str.startswith('中国建设银行'))]
                if not total_bank_jh_sf_df.empty:
                    salary_pay._total_bank_jh_sf += total_bank_jh_sf_df['奖金信息-实发'].iloc[0]

        if '公积金信息-公积金方案' in df.columns:
            tg = df.groupby(
                [utils.tax_column_name, utils.depart_display_column_name, '公积金信息-公积金方案']).sum()
            if '马鞍山钢铁股份有限公司（总部）' == tex_depart:
                if '工资信息-公积金个人额度' in df.columns and '工资信息-公积金企业额度' in df.columns:
                    total_gjj_gh_df = tg.loc[(tg.index.get_level_values(
                        0).str.startswith(tex_depart)) & (tg.index.get_level_values(1).str.startswith(depart)) & (tg.index.get_level_values(2).str.startswith('马鞍山钢铁股份有限公司（总部）公积金方案_1'))]

                    if not total_gjj_gh_df.empty:
                        salary_pay._total_gjj_gh = total_gjj_gh_df['工资信息-公积金个人额度'].iloc[0] + \
                            total_gjj_gh_df['工资信息-公积金企业额度'].iloc[0]
                    total_gjj_jh_df = tg.loc[(tg.index.get_level_values(
                        0).str.startswith(tex_depart)) & (tg.index.get_level_values(1).str.startswith(depart)) & (tg.index.get_level_values(2).str.startswith('马鞍山钢铁股份有限公司（总部）公积金方案_2'))]

                    if not total_gjj_jh_df.empty:
                        salary_pay._total_gjj_jh = total_gjj_jh_df['工资信息-公积金个人额度'].iloc[0] + \
                            total_gjj_jh_df['工资信息-公积金企业额度'].iloc[0]
    return salary_pay


# def create_pdfs(period, departs, merges):
#     for tex_depart, datas_by_tex_depart in merges.items():
#         merge_by_tex_depart(period.period, file_name(
#             period.period, tex_depart), tex_depart, seal_name(tex_depart), datas_by_tex_depart, departs)
#         for depart, datas_by_depart in datas_by_tex_depart.items():
#             merge(period.period, depart, file_name(
#                 period.period, depart), seal_name(tex_depart), datas_by_depart, departs)


def file_name(period, depart):
    return '{}{}{}'.format(depart, period, filename_suffix)


def seal_name(tex_depart):
    if '马钢（集团）控股有限公司(总部)' == tex_depart:
        return "jt"
    elif '马鞍山钢铁股份有限公司（总部）' == tex_depart:
        return "gf"
    else:
        return 'jt'
        # raise ValueError('获取印章图片出错!文件名称{}'.format(tex_depart))


def init_tff():
    # 注册字体
    pdfmetrics.registerFont(TTFont("deng", "Dengb.ttf"))


def filepath(filename, period='', foldername=[]):
    path = file_path_prefix
    if period:
        path = join(path, period)
    if len(foldername) > 0:
        for f in foldername:
            path = join(path, f)
    utils.make_folder_if_nessage(path)
    return join(path, r'{}{}'.format(filename, '.pdf'))


def sealpath(sealname):
    return join(file_path_prefix, r'{}{}'.format(sealname, '.png'))


def get_paragraphstyle(name, font_name, alignment, font_size):
    return ParagraphStyle(name=name,

                          fontName=font_name,

                          alignment=alignment,  # 居中对齐

                          fontSize=font_size)


def get_styles():
    styles = getSampleStyleSheet()
    # 标题样式
    styles.add(get_paragraphstyle('p_title', 'deng', 1, 20))
    # 日期样式
    styles.add(get_paragraphstyle('p_period', 'deng', 2, 12))
    return styles


def create_table_data(salarypay: SalaryPay):
    sealname, departname = salarypay.sealname, salarypay.depart
    if 'gf' == sealname:
        return gf_table_data(salarypay)
    else:
        if '新闻中心' == departname:
            return jtxw_table_data(salarypay)
        elif '教培中心' == departname:
            return jtay_table_data(salarypay)
        return jtbb_table_data(salarypay)


def jtbb_table_data(salarypay: SalaryPay):
    return [['序号', '事由', '项目', '', '金额'],
            ['1', '工资', '工资奖金', '', salarypay.total_sf],
            ['2', '社会保险', '养老保险', '单位数', salarypay.yangl_qy],
            ['', '', '', '个人数', salarypay.yangl_gr],
            ['', '', '', '小计', salarypay.yangl_total()],
            ['', '', '医疗保险', '单位数', salarypay.yil_qy],
            ['', '', '', '个人数', salarypay.yil_gr],
            ['', '', '', '小计', salarypay.yil_total()],
            ['', '', '失业保险', '单位数', salarypay.sy_qy],
            ['', '', '', '个人数', salarypay.sy_gr],
            ['', '', '', '小计', salarypay.sy_total()],
            ['', '', '工伤保险', '单位数', salarypay.gs],
            ['', '', '生育保险', '单位数', salarypay.sy],
            ['', '', '社保合计', '', salarypay.bx_total()],
            ['3', '住房公积金', '', '单位数', salarypay.gjj_qy],
            ['', '', '', '个人数', salarypay.gjj_gr],
            ['', '', '', '小计', salarypay.gjj_total()],
            ['4', '企业年金', '', '单位数', salarypay.nj_qy],
            ['', '', '', '个人数', salarypay.nj_gr],
            ['', '', '', '小计', salarypay.nj_total()],
            ['5', '合计', '', '', salarypay.total()],
            ['6', '其中：拨付中行户4528（工资奖金）', '', '', salarypay.total_bank_zh_sf],
            ['', '拨付工行户3435（工资奖金）', '', '', salarypay.total_bank_gh_sf],
            ['', '拨付建行户（工资奖金）', '', '', salarypay.total_bank_jh_sf],
            ['', ' 拨付财务公司户9105（社保、住房公积金、企业年金）', '', '', round(salarypay.bx_total()+salarypay.gjj_total()+salarypay.nj_total(), 2)], ]


def jtay_table_data(salarypay: SalaryPay):

    return [['序号', '事由', '项目', '', '金额'],
            ['1', '工资', '工资奖金', '', salarypay.total_sf],
            ['2', '社会保险', '养老保险', '单位数', salarypay.yangl_qy],
            ['', '', '', '个人数', salarypay.yangl_gr],
            ['', '', '', '小计', salarypay.yangl_total()],
            ['', '', '医疗保险', '单位数', salarypay.yil_qy],
            ['', '', '', '个人数', salarypay.yil_gr],
            ['', '', '', '小计', salarypay.yil_total()],
            ['', '', '失业保险', '单位数', salarypay.sy_qy],
            ['', '', '', '个人数', salarypay.sy_gr],
            ['', '', '', '小计', salarypay.sy_total()],
            ['', '', '工伤保险', '单位数', salarypay.gs],
            ['', '', '生育保险', '单位数', salarypay.sy],
            ['', '', '社保合计', '', salarypay.bx_total()],
            ['3', '住房公积金', '', '单位数', salarypay.gjj_qy],
            ['', '', '', '个人数', salarypay.gjj_gr],
            ['', '', '', '小计', salarypay.gjj_total()],
            ['4', '企业年金', '', '单位数', salarypay.nj_qy],
            ['', '', '', '个人数', salarypay.nj_gr],
            ['', '', '', '小计', salarypay.nj_total()],
            ['5', '合计', '', '', salarypay.total()],
            ['6', '其中：拨付工行户1073（工资奖金）', '', '', salarypay.total_sf],
            ['', ' 拨付财务公司户9378（社保、住房公积金、企业年金）', '', '', round(salarypay.bx_total()+salarypay.gjj_total()+salarypay.nj_total(), 2)], ]


def jtxw_table_data(salarypay: SalaryPay):

    return [['序号', '事由', '项目', '', '金额'],
            ['1', '工资', '工资奖金', '', salarypay.total_sf],
            ['2', '社会保险', '养老保险', '单位数', salarypay.yangl_qy],
            ['', '', '', '个人数', salarypay.yangl_gr],
            ['', '', '', '小计', salarypay.yangl_total()],
            ['', '', '医疗保险', '单位数', salarypay.yil_qy],
            ['', '', '', '个人数', salarypay.yil_gr],
            ['', '', '', '小计', salarypay.yil_total()],
            ['', '', '失业保险', '单位数', salarypay.sy_qy],
            ['', '', '', '个人数', salarypay.sy_gr],
            ['', '', '', '小计', salarypay.sy_total()],
            ['', '', '工伤保险', '单位数', salarypay.gs],
            ['', '', '生育保险', '单位数', salarypay.sy],
            ['', '', '社保合计', '', salarypay.bx_total()],
            ['3', '住房公积金', '', '单位数', salarypay.gjj_qy],
            ['', '', '', '个人数', salarypay.gjj_gr],
            ['', '', '', '小计', salarypay.gjj_total()],
            ['4', '企业年金', '', '单位数', salarypay.nj_qy],
            ['', '', '', '个人数', salarypay.nj_gr],
            ['', '', '', '小计', salarypay.nj_total()],
            ['5', '合计', '', '', salarypay.total()],
            ['6', '其中：拨付中行户5668（工资奖金）', '', '', salarypay.total_sf],
            ['', ' 拨付财务公司户9106（社保、住房公积金、企业年金）', '', '', round(salarypay.bx_total()+salarypay.gjj_total()+salarypay.nj_total(), 2)], ]


def gf_table_data(salarypay: SalaryPay):
    return [['序号', '事由', '项目', '', '金额'],
            ['1', '工资', '工资奖金', '', salarypay.total_sf],
            ['2', '社会保险\n财务公司户9103(社保)', '养老保险', '单位数', salarypay.yangl_qy],
            ['', '', '', '个人数', salarypay.yangl_gr],
            ['', '', '', '小计', salarypay.yangl_total()],
            ['', '', '医疗保险', '单位数', salarypay.yil_qy],
            ['', '', '', '个人数', salarypay.yil_gr],
            ['', '', '', '小计', salarypay.yil_total()],
            ['', '', '失业保险', '单位数', salarypay.sy_qy],
            ['', '', '', '个人数', salarypay.sy_gr],
            ['', '', '', '小计', salarypay.sy_total()],
            ['', '', '工伤保险', '单位数', salarypay.gs],
            ['', '', '生育保险', '单位数', salarypay.sy],
            ['', '', '社保合计', '', salarypay.bx_total()],
            ['3', '住房公积金', '', '单位数', salarypay.gjj_qy],
            ['', '', '', '个人数', salarypay.gjj_gr],
            ['', '', '', '小计', salarypay.gjj_total()],
            ['4', '企业年金', '', '单位数', salarypay.nj_qy],
            ['', '', '', '个人数', salarypay.nj_gr],
            ['', '', '', '小计', salarypay.nj_total()],
            ['5', '合计', '', '', salarypay.total()],
            ['6', '其中：拨付中行户178206214933（工资奖金）', '',
                '', salarypay.total_bank_zh_sf],
            ['', '拨付工行户1306020409022100424（工资奖金）',
                '', '', salarypay.total_bank_gh_sf],
            ['', '拨付建行户34001658808050330058（工资奖金）',
                '', '', salarypay.total_bank_jh_sf],
            ['', '拨付财务公司户9103（社保）', '', '', salarypay.bx_total()],
            ['', '拨付财务公司户5005（企业年金）', '', '', salarypay.nj_total()],
            ['', '拨付工行四村支行 马鞍山市住房公积金管理中心\n马钢（集团）控股公司分中心 1306021309300003582（工行公积金）',
                '', '', salarypay.total_gjj_gh],
            ['', '拨付建行团结广场支行  马鞍山市住房公积金管理中心\n马钢(集团)控股有限公司分中心 34001654308050345135 （建行公积金）', '', '', salarypay.total_gjj_jh], ]


def gf_table_styles():
    return TableStyle([('GRID', (0, 0), (-1, -1), 1, colors.grey),
                       ('FONT', (0, 0), (-1, -1), 'deng'),
                       ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                       #    ('ALIGN', (0, 1), (-2, -1), 'LEFT'),
                       ('VALIGN', (0, 1), (-2, -1), 'MIDDLE'),
                       ('SPAN', (2, 0), (3, 0)),
                       ('SPAN', (2, 1), (3, 1)),
                       ('SPAN', (1, 2), (1, 13)),
                       ('SPAN', (2, 2), (2, 4)),
                       ('SPAN', (2, 5), (2, 7)),
                       ('SPAN', (2, 8), (2, 10)),
                       ('SPAN', (2, 13), (3, 13)),
                       ('SPAN', (1, 14), (2, 16)),
                       ('SPAN', (1, 17), (2, 19)),
                       ('SPAN', (1, 20), (3, 20)),
                       ('SPAN', (1, 21), (3, 21)),
                       ('SPAN', (1, 22), (3, 22)),
                       ('SPAN', (1, 23), (3, 23)),
                       ('SPAN', (1, 24), (3, 24)),
                       ('SPAN', (1, 25), (3, 25)),
                       ('SPAN', (1, 26), (3, 26)),
                       ('SPAN', (1, 27), (3, 27)),
                       ('SPAN', (0, 2), (0, 13)),
                       ('SPAN', (0, 14), (0, 16)),
                       ('SPAN', (0, 17), (0, 19)),
                       ('SPAN', (0, 21), (0, 27)),
                       ])


def jtbb_table_styles():
    return TableStyle([('GRID', (0, 0), (-1, -1), 1, colors.grey),
                       ('FONT', (0, 0), (-1, -1), 'deng'),
                       ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                       #    ('ALIGN', (0, 1), (-2, -1), 'LEFT'),
                       ('VALIGN', (0, 1), (-2, -1), 'MIDDLE'),
                       ('SPAN', (2, 0), (3, 0)),
                       ('SPAN', (2, 1), (3, 1)),
                       ('SPAN', (1, 2), (1, 13)),
                       ('SPAN', (2, 2), (2, 4)),
                       ('SPAN', (2, 5), (2, 7)),
                       ('SPAN', (2, 8), (2, 10)),
                       ('SPAN', (2, 13), (3, 13)),
                       ('SPAN', (1, 14), (2, 16)),
                       ('SPAN', (1, 17), (2, 19)),
                       ('SPAN', (1, 20), (3, 20)),
                       ('SPAN', (1, 21), (3, 21)),
                       ('SPAN', (1, 22), (3, 22)),
                       ('SPAN', (1, 23), (3, 23)),
                       ('SPAN', (0, 2), (0, 13)),
                       ('SPAN', (0, 14), (0, 16)),
                       ('SPAN', (0, 17), (0, 19)),
                       ('SPAN', (0, 21), (0, 23)),
                       ])


def jtqt_table_styles():
    # 集团 教培  新闻
    return TableStyle([('GRID', (0, 0), (-1, -1), 1, colors.grey),
                       ('FONT', (0, 0), (-1, -1), 'deng'),
                       ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                       #    ('ALIGN', (0, 1), (-2, -1), 'LEFT'),
                       ('VALIGN', (0, 1), (-2, -1), 'MIDDLE'),
                       ('SPAN', (2, 0), (3, 0)),
                       ('SPAN', (2, 1), (3, 1)),
                       ('SPAN', (1, 2), (1, 13)),
                       ('SPAN', (2, 2), (2, 4)),
                       ('SPAN', (2, 5), (2, 7)),
                       ('SPAN', (2, 8), (2, 10)),
                       ('SPAN', (2, 13), (3, 13)),
                       ('SPAN', (1, 14), (2, 16)),
                       ('SPAN', (1, 17), (2, 19)),
                       ('SPAN', (1, 20), (3, 20)),
                       ('SPAN', (1, 21), (3, 21)),
                       ('SPAN', (1, 22), (3, 22)),
                       ('SPAN', (0, 2), (0, 13)),
                       ('SPAN', (0, 14), (0, 16)),
                       ('SPAN', (0, 17), (0, 19)),
                       ('SPAN', (0, 21), (0, 22)),
                       ])


def create_table_styles(sealname, departname):
    if 'gf' == sealname:
        return gf_table_styles()
    else:
        if '新闻中心' == departname or '教培中心' == departname:
            return jtqt_table_styles()
        return jtbb_table_styles()


def create_salary_pay_app_form(salarypay: SalaryPay, filename, hz=False):
    # 创建薪酬发放申请单pdf文件

    init_tff()
    default_styles = get_styles()
    period, sealname, departname = salarypay.period, salarypay.sealname, salarypay.depart
    title_p1 = Paragraph(departname, default_styles['p_title'])
    title_p2 = Paragraph("{}工资费用资金调拨单".format(
        period), default_styles['p_title'])

    period_p = Paragraph("申请日期:  {}".format(
        period), default_styles['p_period'])

    # table
    data = create_table_data(salarypay)

    table_styles = create_table_styles(sealname, departname)
    table = Table(data=data, style=table_styles,
                  colWidths=(0.5*inch, 1.8*inch, 1.5*inch, 1.5*inch, 1.5*inch))
    filename_temp = r'{}{}'.format(filename, '_temp')
    doc = SimpleDocTemplate(
        filepath(filename_temp, period, ["系统导出", utils.pdf_folder_name, departname]), pagesize=A4)

    elements = []
    elements.append(title_p1)
    elements.append(Spacer(0, 0.2*inch))
    elements.append(title_p2)
    elements.append(Spacer(0, 0.5*inch))
    elements.append(period_p)
    elements.append(Spacer(0, 0.2*inch))
    elements.append(table)

    doc.build(elements)

    return filename_temp


def create_salary_pay_app_form_1():
    # 创建薪酬发放申请单pdf文件

    init_tff()
    default_styles = get_styles()
    period, sealname, departname = '202201', 'jt', '集团机关'
    title_p1 = Paragraph(departname, default_styles['p_title'])
    title_p2 = Paragraph("{}工资费用资金调拨单".format(
        period), default_styles['p_title'])

    period_p = Paragraph("申请日期:  {}".format(
        period), default_styles['p_period'])

    # table
    # data = create_table_data(salarypay)

    table_styles = create_table_styles(sealname, departname)
    # table = Table(data=data, style=table_styles,
    #               colWidths=(0.5*inch, 1.8*inch, 1.5*inch, 1.5*inch, 1.5*inch))
    filename_temp = r'{}{}'.format('调拨但', '_temp')
    doc = SimpleDocTemplate(
        "D:\\薪酬审核文件夹\\202201\\系统导出\\拨款单\\马钢（集团）控股有限公司(总部)\\马钢（集团）控股有限公司(总部)202201工资费用资金调拨单_temp.pdf", pagesize=A4)

    elements = []
    elements.append(title_p1)
    elements.append(Spacer(0, 0.2*inch))
    elements.append(title_p2)
    elements.append(Spacer(0, 0.5*inch))
    elements.append(period_p)
    elements.append(Spacer(0, 0.2*inch))

    doc.build(elements)

    return filename_temp


def create_seal_pdf(sealname):
    seal_path = sealpath(sealname)
    sealname_temp = r'{}{}'.format(sealname, '_temp')
    c = canvas.Canvas(filepath(sealname_temp), pagesize=A4)
    c.drawImage(seal_path, 13 * cm, 23 * cm, 6 * cm,
                5 * cm, mask='auto')
    c.showPage()
    c.save()
    return sealname_temp


def to_tax_depart_new(period, filename, tex_depart, sealname, salary_pay, hz=True):
    filename_temp = create_salary_pay_app_form(salary_pay, filename, hz)
    sealname_temp = create_seal_pdf(sealname)
    op_pdf = PdfFileWriter()
    pay_pdf = PdfFileReader(
        open(filepath(filename_temp, period, ['系统导出', utils.pdf_folder_name, tex_depart]), 'rb'))
    seal_pdf = PdfFileReader(open(filepath(sealname_temp), 'rb'))
    page = pay_pdf.getPage(0)
    page.mergePage(seal_pdf.getPage(0))
    page.compressContentStreams()  # 压缩内容
    op_pdf.addPage(page)

    with open(filepath(filename, period, ['系统导出', utils.pdf_folder_name, tex_depart]), 'wb') as out:
        op_pdf.write(out)


# def merge_by_tex_depart(period, filename, tex_depart, sealname, merges, departs):
#     salary_pay = SalaryPay().to_salary_pay_group_by_tex_depart(
#         period, tex_depart, sealname, merges, departs)
#     filename_temp = create_salary_pay_app_form(salary_pay, filename, True)
#     sealname_temp = create_seal_pdf(sealname)
#     op_pdf = PdfFileWriter()
#     pay_pdf = PdfFileReader(
#         open(filepath(filename_temp, period, ['汇总数据', tex_depart]), 'rb'))
#     seal_pdf = PdfFileReader(open(filepath(sealname_temp), 'rb'))
#     page = pay_pdf.getPage(0)
#     page.mergePage(seal_pdf.getPage(0))
#     page.compressContentStreams()  # 压缩内容
#     op_pdf.addPage(page)

#     with open(filepath(filename, period, ['汇总数据', tex_depart]), 'wb') as out:
#         op_pdf.write(out)


# def merge(period, depart, filename, sealname, merges, departs):
#     salary_pay = SalaryPay().to_salary_pay_group_by_depart(
#         period, depart,  sealname, merges, departs)
#     filename_temp = create_salary_pay_app_form(salary_pay, filename)
#     sealname_temp = create_seal_pdf(sealname)
#     op_pdf = PdfFileWriter()
#     pay_pdf = PdfFileReader(
#         open(filepath(filename_temp, period, [depart]), 'rb'))
#     seal_pdf = PdfFileReader(open(filepath(sealname_temp), 'rb'))
#     page = pay_pdf.getPage(0)
#     page.mergePage(seal_pdf.getPage(0))
#     page.compressContentStreams()  # 压缩内容
#     op_pdf.addPage(page)

#     with open(filepath(filename, period, [depart]), 'wb') as out:
#         op_pdf.write(out)


if __name__ == '__main__':
    pass
    # merge('202106', '01_集团机关', "demo", "gf", {}, {})
