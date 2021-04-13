#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   stack.py
@Time    :   2021/04/08 15:02:41
@Author  :   Tong tan 
@Version :   1.0
@Contact :   tongtan@gmail.com
'''


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
