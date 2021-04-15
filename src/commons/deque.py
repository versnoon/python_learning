#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   deque.py
@Time    :   2021/04/15 12:10:04
@Author  :   Tong tan 
@Version :   1.0
@Contact :   tongtan@gmail.com
'''


def pai_check(pai_str):
    deque = Deque()

    for c in pai_str:
        deque.add_rear(c)

    eq = True

    while deque.size() > 1 and eq:
        front = deque.remove_front()
        end = deque.remove_rear()
        if front != end:
            eq = False
    return eq


class Deque:
    """
    双端队列
    """

    def __init__(self):
        self.items = []

    def is_empty(self):
        return self.items == []

    def add_front(self, item):
        self.items.append(item)

    def add_rear(self, item):
        self.items.insert(0, item)

    def remove_front(self):
        return self.items.pop()

    def remove_rear(self):
        return self.items.pop(0)

    def size(self):
        return len(self.items)
