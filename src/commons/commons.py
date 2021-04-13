#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   commons.py
@Time    :   2021/03/26 13:13:49
@Author  :   Tong tan
@Version :   1.0
@Contact :   tongtan@gmail.com
'''

from types import MethodType
import os
import turtle
from collections.abc import Iterator

from src.commons.stack import Stack


def match(open, close):
    opens = "([{"
    closes = ")]}"
    return opens.index(open) == closes.index(close)


def par_checker(symbol_str):
    """
    匹配符号
    """
    s = Stack()
    blanced = True
    index = 0

    while index < len(symbol_str) and blanced:
        symble = symbol_str[index]
        if symble in '([{':
            s.push(symble)
        else:
            if s.is_empty():
                blanced = False
            else:
                top = s.pop()
                if not match(top, symble):
                    blanced = False
        index = index + 1

    if blanced and s.is_empty():
        return True
    else:
        return False


class Student:
    # pass
    __slots__ = ('age', 'score', 'Name', 'set_score')


def set_score(self, score):
    self.score = score


if __name__ == "__main__":
    # s = Student()
    # s.Name = "TT"
    # print(s.Name)
    # s.set_score = MethodType(set_score, s)
    # s.set_score(90)
    # print(s.score)
    # # s2 = Student()
    # # s2.set_score(80)
    # print(os.name)
    # print(os.environ)
    turtle.width(4)
    turtle.forward(200)
    turtle.right(90)

    turtle.pencolor('red')
    turtle.forward(100)
    turtle.right(90)

    turtle.pencolor('green')
    turtle.forward(200)
    turtle.right(90)

    turtle.pencolor('blue')
    turtle.forward(100)
    turtle.right(90)

    turtle.done()
