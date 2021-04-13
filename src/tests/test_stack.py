#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   test_stack.py
@Time    :   2021/04/13 14:32:04
@Author  :   Tong tan 
@Version :   1.0
@Contact :   tongtan@gmail.com
'''

from src.commons.stack import Stack, par_checker, divide_by_base, infix_to_postfix


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

    def test_divide_by_base(self):

        assert "1" == divide_by_base(1, 2)
        assert "1100100" == divide_by_base(100, 2)
        assert "144" == divide_by_base(100, 8)
        assert "64" == divide_by_base(100, 16)
        assert "F" == divide_by_base(15, 16)

    def test_infix_to_postfix(self):

        assert "AB+CD+*" == infix_to_postfix("( A + B ) * ( C + D )")
        assert "AB+C*" == infix_to_postfix("( A + B ) * C")
        assert "ABC*+" == infix_to_postfix("A + B * C")
