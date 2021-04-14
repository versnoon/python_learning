#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   test_queue.py
@Time    :   2021/04/14 14:32:14
@Author  :   Tong tan 
@Version :   1.0
@Contact :   tongtan@gmail.com
'''

from src.commons.queue import hot_potato


class TestQueue:

    def test_hot_potato(self):
        assert "Susan" == hot_potato(
            ["Bill", "David", "Susan", "Jan", "Kent", "Brad"], 7)
