#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   test_stack.py
@Time    :   2021/04/13 14:32:04
@Author  :   Tong tan 
@Version :   1.0
@Contact :   tongtan@gmail.com
'''

from src.commons.stack import Stack, par_checker


class TestStack:

    def test_stack(self):
        stack = Stack()
        assert stack != None
        assert stack.is_empty()
        stack.push(10)
        i = stack.peek()
        assert i == 10
        assert 1 == stack.size()
        i = stack.pop()
        assert i == 10
        assert 0 == stack.size()

    def test_par_checker(self):
        assert par_checker('()')
        assert not par_checker('(]')
        assert par_checker('((((([{{{{}}}}])))))')
        assert not par_checker('((((([{{{{}}}}]))))]')
