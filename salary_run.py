#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   salary_run.py
@Time    :   2021/10/28 10:42:22
@Author  :   Tong tan 
@Version :   1.0
@Contact :   tongtan@gmail.com
'''


import datetime
import src.salarys.done as run


if __name__ == '__main__':
    # starttime = datetime.datetime.now()
    # ----  人员信息对比
    # run.compare_person()

    # ----  数据效验
    run.audit()

    # ----  导出拨款单
    # run.to_salary_pdf()
    # endtime = datetime.datetime.now()
    # print(endtime - starttime)
    print('done')
