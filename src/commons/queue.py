#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   queue.py
@Time    :   2021/04/14 13:54:50
@Author  :   Tong tan 
@Version :   1.0
@Contact :   tongtan@gmail.com
'''


def hot_potato(name_list, count):
    q = Queue()
    for name in name_list:
        q.enqueue(name)

    while q.size() > 1:
        for i in range(count):
            q.enqueue(q.dequeue())

        q.dequeue()

    return q.dequeue()


class Queue:

    def __init__(self):
        self.items = []

    def is_empty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0, item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)
