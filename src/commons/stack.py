#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   stack.py
@Time    :   2021/04/08 15:02:41
@Author  :   Tong tan 
@Version :   1.0
@Contact :   tongtan@gmail.com
'''

import string


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


def divide_by_base(dec_num, base):
    """
    十进制数转换
    """
    s = Stack()
    digits = "0123456789ABCDEF"
    while dec_num > 0:
        rem = dec_num % base
        s.push(rem)
        dec_num = dec_num // base

    bin_str = ""
    while not s.is_empty():
        bin_str = bin_str + digits[s.pop()]

    return bin_str


def infix_to_postfix(infix_expr):
    """
    中序转后续表达式
    """
    prec = {}
    prec["*"] = 3
    prec["/"] = 3
    prec["+"] = 2
    prec["-"] = 2
    prec["("] = 1

    s = Stack()
    postfix_list = []

    token_list = infix_expr.split()

    for token in token_list:
        if token in string.ascii_uppercase:
            postfix_list.append(token)
        elif token == "(":
            s.push(token)
        elif token == ")":
            top = s.pop()
            while top != "(":
                postfix_list.append(top)
                top = s.pop()
        else:
            while (not s.is_empty()) and (prec[s.peek()] >= prec[token]):
                postfix_list.append(s.pop())
            s.push(token)
    while not s.is_empty():
        postfix_list.append(s.pop())
    return "".join(postfix_list)


def postfix_eval(postfix_expr):
    s = Stack()

    token_list = postfix_expr.split()

    for token in token_list:
        if token in "0123456789":
            s.push(int(token))
        else:
            ope_2 = s.pop()
            ope_1 = s.pop()
            res = do_math(token, ope_1, ope_2)
            s.push(res)
    return s.pop()


def do_math(op, ope_1, ope_2):
    if op == "*":
        return ope_1 * ope_2
    if op == "/":
        return ope_1 / ope_2
    if op == "+":
        return ope_1 + ope_2
    if op == "-":
        return ope_1 + ope_2


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
