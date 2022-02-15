#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   report.py
@Time    :   2021/05/07 10:54:32
@Author  :   Tong tan
@Version :   1.0
@Contact :   tongtan@gmail.com
'''
import time

from os.path import exists
from os import makedirs

import xlwt


class ReportColumn:

    def __init__(self, names=[], sort_no=-1, code=""):
        # 列的名称 用数组存储 用于定义复杂复杂表头
        self.names = names
        # 显示序号
        self.sort_no = sort_no
        # 对应属性 用于反射获取数值
        self.code = code


class ReportCell:
    """
    报表单元格定义
    """

    def __init__(self, contant, row_start_no=-1, col_start_no=-1, row_offset=0, col_offset=0, styles=None):
        # 显示得内容
        self.contant = contant
        self.row_start_no = row_start_no
        self.row_offset = row_offset
        self.col_start_no = col_start_no
        self.col_offset = col_offset
        # 内容格式 默认为 字符型 S
        self.contant_type = "S"
        self.styles = styles

    def get_contant(self):
        """
        根据内容格式获取标准化输出
        """
        if self.contant != None:
            if self.contant_type == "S" and isinstance(self.contant, str):
                return self.get_str_val()
            elif self.contant_type == "I" and isinstance(self.contant, int):
                return self.get_int_val()
            elif self.contant_type == "F" and isinstance(self.contant, float):
                return self.get_float_val()
            else:
                return self.get_default_val()
        else:
            return ""

    def get_str_val(self):
        """
        获取字符串显示
        """
        return self.contant.strip()

    def get_int_val(self):
        return self.get_default_val()

    def get_float_val(self):
        """
        默认保留两位
        """
        return round(self.contant, 2)

    def get_default_val(self):
        return self.contant


class Report:

    EXT = "xlsx"

    def __init__(self, period=None, name="报表名称", title="标题", creator="人力资源服务中心薪酬发放室", datas=[], title_showable=True):
        # 报表名称
        self.name = name
        # 编报单位
        self.creator = creator
        # 报表标题
        self.title = title
        # 报表列定义数组
        self.columns = []
        # 报表数据
        self.datas = datas

        # 是否显示标题编报等信息
        self.title_showable = title_showable

        # 报表日期 默认为当前日期
        self.date_info = self.date_info_str()

        # 保存路径前缀
        self.base_folder_prefix = r'd:\薪酬审核文件夹'

        # 审核日期
        self.period = period

    def add_column(self, col: ReportColumn):
        if not isinstance(col, ReportColumn):
            self.columns.clear()
            raise TypeError(
                "report column define err,column is not ReportColumn type")
        self.columns.append(col)

    def add_columns(self, cols):
        for col in cols:
            if isinstance(col, ReportColumn):
                self.add_column(col)
            else:
                self.columns.clear()
                raise TypeError(
                    "report column define err,column is not ReportColumn type")

    def report_columns(self):
        """
        获取报表列定义
        """
        return tuple(self.columns)

    def date_info_str(self):
        return time.strftime("%Y年%m月%d日", time.localtime())

    def sheetname(self):
        return "Sheet1"

    def report_filename(self):
        return self.name

    def parse_report(self):
        # 是否显示
        title_showable = self.title_showable
        max_clo_no, max_row_no, col_name_size = self.parse_title_columns()
        return title_showable, max_clo_no, max_row_no, col_name_size

    def parse_title_columns(self):
        columns = self.report_columns()
        # 报表导出需要多少列
        max_col_no = len(columns)
        # 报表提头最多需要多少行
        max_row_no = 1
        cols = {}
        for col in columns:
            # 获取列头最大行数
            col_names = col.names
            col_size = len(col_names)
            if max_row_no < col_size:
                max_row_no = col_size
            for name in col_names:
                size = 1
                if name in cols:
                    size = cols[name]
                    size += 1
                cols[name] = size
        return max_col_no, max_row_no, cols

    def export(self, folders=[]):

        b = xlwt.Workbook(encoding='uft-8')
        s = b.add_sheet(self.sheetname())

        # 默认从0行0列开始输出报表
        start_row_no = 0
        start_col_no = 0

        title_showable, max_col_no, max_row_no, col_name_size = self.parse_report()
        report_cells = []

        # 创建报表标题报表单元格
        # 创建报表描述行
        # 创建空行
        if title_showable:
            report_cells.extend(self.create_title_report_cells(
                max_col_no, start_row_no, start_col_no))
            self.blank_row(start_row_no+3, s)
            start_row_no += 4
        # 创建报表列名单元格
        report_cells.extend(self.create_columns_report_cells(
            start_row_no,  max_row_no, col_name_size))
        start_row_no += max_row_no
        # 创建数据项目
        report_cells.extend(self.create_datas_report_cells(start_row_no))

        # 写入报表
        self.write_cell(s, report_cells)

        path = r'{}\{}\{}'.format(
            self.base_folder_prefix, self.period, "相关报表")
        if not self.period:
            path = self.base_folder_prefix
        if len(folders) > 0:
            for folder in folders:
                path = f'{path}\{folder}'
        if not exists(path):
            makedirs(path)
        b.save(r'{}\{}.{}'.format(path, self.report_filename(), self.EXT))

    def create_title_report_cells(self, max_col_no, start_row_no, start_col_no):
        return [ReportCell(
            self.title, start_row_no, start_col_no, 0, max_col_no-1, self.head_styles()), ReportCell(f'编报:{self.creator}', start_row_no+2, 0), ReportCell(f'编制如期:{self.date_info}', start_row_no+2, max_col_no-3)]

        # self.write_cell(sheet, [report_name])

    def create_columns_report_cells(self, start_row_no, max_row_no, col_name_size):
        columns = self.report_columns()
        res_cols = {}
        res_cells = []
        for col in columns:
            res_cells.extend(self.create_column_report_cells(
                col, start_row_no, max_row_no, col_name_size))
        for cell in res_cells:
            col_name = cell.get_contant()
            if not col_name in res_cols:
                res_cols[col_name] = cell
        return res_cols.values()

    def create_column_report_cells(self, col, start_row_no, max_row_no, col_name_size):
        col_names = col.names
        sort_no = col.sort_no
        col_size = len(col_names)
        col_star_row = start_row_no
        res = []
        styles = self.title_styles()
        for i, col_name in enumerate(col_names):
            col_height = len(col_names)
            row_offset = max_row_no - i - 1
            if i != col_height - 1:
                row_offset = 0
            res.append(ReportCell(
                col_name, col_star_row+i, sort_no, row_offset, col_name_size[col_name] - 1, styles))
        return res

    def create_datas_report_cells(self, start_row_no):
        styles = self.contant_styles()
        res = []
        for i, data in enumerate(self.datas):
            res.extend(self.create_data_row_report_cells(
                data, start_row_no+i, styles))
        return res

    def create_data_row_report_cells(self, data, start_row_no, styles):
        columns = self.report_columns()
        res = []
        # styles = self.contant_styles()
        for col in columns:
            # 获取对应的属性
            code = col.code
            # 反射获取属性值
            contant = self.get_report_cell_val(data, code)
            if contant != None:
                res.append(ReportCell(contant, start_row_no,
                                      col.sort_no, 0, 0, styles))
        return res

    def get_report_cell_val(self, data, code):
        if hasattr(data, code):
            return getattr(data, code)

    def write_cell(self, sheet, cells):
        default_styles = self.default_styles()
        for cell in cells:
            row_start_no = cell.row_start_no
            col_start_no = cell.col_start_no
            styles = cell.styles
            if not styles:
                styles = default_styles
            # 单元格其实坐标为-1 时报错
            if row_start_no == -1 or col_start_no == -1:
                raise ValueError(
                    f'cell Coordinates err: row_no{row_start_no},col_no{col_start_no}')
            if cell.col_offset == 0 and cell.row_offset == 0:
                sheet.write(row_start_no, col_start_no,
                            cell.get_contant(), styles)
            else:
                sheet.write_merge(row_start_no, row_start_no+cell.row_offset,
                                  col_start_no, col_start_no+cell.col_offset, cell.get_contant(), styles)

    def default_styles(self):
        return xlwt.XFStyle()

    def head_styles(self):
        style = xlwt.XFStyle()  # 创建一个样式对象，初始化样式
        al = xlwt.Alignment()
        al.horz = 0x02      # 设置水平居中
        al.vert = 0x01      # 设置垂直居中
        style.alignment = al
        fnt = xlwt.Font()
        fnt.name = u'微软雅黑'  # 设置其字体为微软雅黑
        fnt.colour_index = 0  # 设置其字体颜色黑色
        fnt.bold = True  # 加粗
        fnt.height = 20*18  # 字体大小
        style.font = fnt
        return style

    def min_height_styles(self):
        return xlwt.easyxf(r'font:height {};'.format(20*3))

    def title_styles(self):
        style = xlwt.XFStyle()  # 创建一个样式对象，初始化样式
        al = xlwt.Alignment()
        al.horz = 0x02      # 设置水平居中
        al.vert = 0x01      # 设置垂直居中
        al.wrap = 1  # 自动换行
        style.alignment = al
        fnt = xlwt.Font()
        fnt.name = u'Arial'  # 设置其字体为微软雅黑
        fnt.colour_index = 0  # 设置其字体颜色黑色
        fnt.bold = True  # 加粗
        fnt.height = 20*10  # 字体大小
        style.font = fnt
        borders = xlwt.Borders()
        borders.left = 1
        borders.top = 1
        borders.right = 1
        borders.bottom = 1
        style.borders = borders
        return style

    def contant_styles(self):
        style = xlwt.XFStyle()  # 创建一个样式对象，初始化样式
        al = xlwt.Alignment()
        al.horz = 0x02      # 设置水平居中
        al.vert = 0x01      # 设置垂直居中
        al.wrap = 1  # 自动换行
        style.alignment = al
        fnt = xlwt.Font()
        fnt.name = u'Arial'  # 设置其字体为微软雅黑
        fnt.colour_index = 0  # 设置其字体颜色黑色
        # fnt.bold = True  # 加粗
        fnt.height = 20*10  # 字体大小
        style.font = fnt
        borders = xlwt.Borders()
        borders.left = 1
        borders.top = 1
        borders.right = 1
        borders.bottom = 1
        style.borders = borders
        return style

    def blank_row(self, row_no, sheet):
        sheet.row(row_no).set_style(self.min_height_styles())
