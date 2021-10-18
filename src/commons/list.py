#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   list.py
@Time    :   2021/04/15 12:30:32
@Author  :   Tong tan 
@Version :   1.0
@Contact :   tongtan@gmail.com
'''


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

    def get_data(self):
        return self.data

    def get_next(self):
        return self.next

    def set_data(self, data):
        self.data = data

    def set_next(self, n):
        self.next = n


class UnorderList:

    def __init__(self):
        self.head = None

    def is_empty(self):
        return self.head == None

    def add(self, data):
        n = Node(data)
        n.set_next(self.head)
        self.head = n

    def size(self):
        current = self.head
        count = 0
        while current != None:
            count += 1
            current = current.get_next()
        return count

    def search(self, data):
        c = self.head
        found = False
        while c != None and not found:
            if c.get_data() == data:
                found = True
            else:
                c = c.get_next()
        return found

    def remove(self, data):
        c = self.head
        pre = None
        found = False
        while c != None and not found:
            if c.get_data() == data:
                found = True
            else:
                pre = c
                c = c.get_next()
        if found:
            if pre == None:
                self.head = c.get_next()
            else:
                pre.set_next(c.get_next())

    def append(self, data):
        c = self.head
        n = Node(data)
        while c != None:
            c = c.get_next()
        # 链表头节点
        if c == None:
            self.head = n
        else:
            c.set_next(n)

    def insert(self, index, data):
        c = self.head
        pre = None
        n = Node(data)
        count = 0
        while c != None:
            pre = c
            c = c.get_next()
            if count == index:
                break
            count = count + 1
        if c == None and index != 0:
            raise IndexError(f'')
