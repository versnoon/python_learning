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
    starttime = datetime.datetime.now()
    run.load_data()
    endtime = datetime.datetime.now()
    print(endtime - starttime)
    print('done')
