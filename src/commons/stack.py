#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   stack.py
@Time    :   2021/04/08 15:02:41
@Author  :   Tong tan 
@Version :   1.0
@Contact :   tongtan@gmail.com
'''


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


class Stack:

    def __init__(self):
        self.items = []

    def is_empty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[len(self.items) - 1]

    def size(self):
        return len(self.items)
