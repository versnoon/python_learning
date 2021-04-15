#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   test_deque.py
@Time    :   2021/04/15 12:25:06
@Author  :   Tong tan 
@Version :   1.0
@Contact :   tongtan@gmail.com
'''

from src.commons.deque import pai_check


class TestDeque:

    def test_pai_check(self):
        assert pai_check("ede")
        assert not pai_check("ed")
        assert pai_check("")
