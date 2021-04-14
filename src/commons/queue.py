#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   queue.py
@Time    :   2021/04/14 13:54:50
@Author  :   Tong tan 
@Version :   1.0
@Contact :   tongtan@gmail.com
'''


import random


def hot_potato(name_list, count):
    q = Queue()
    for name in name_list:
        q.enqueue(name)

    while q.size() > 1:
        for i in range(count):
            q.enqueue(q.dequeue())

        q.dequeue()

    return q.dequeue()


def create_new_task():
    num = random.randrange(1, 181)
    if num == 180:
        return True
    return False


def simulation(num_seconds, pages_per_minute):
    labprinter = Printer(pages_per_minute)
    print_queue = Queue()
    wait_times = []

    for current_second in range(num_seconds):
        if create_new_task():
            task = Task(current_second)
            print_queue.enqueue(task)
        if (not labprinter.busy() and (not print_queue.is_empty())):
            next_task = print_queue.dequeue()
            wait_times.append(next_task.wait_times(current_second))
            labprinter.start_next(next_task)
        labprinter.tick()

    average_wait = sum(wait_times) / len(wait_times)
    print("Average Wait %6.2f secs %3d tasks remaining." %
          (average_wait, print_queue.size()))


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


class Printer:
    def __init__(self, ppm):
        self.pagerate = ppm
        self.current_task = None
        self.time_remaining = 0

    def tick(self):
        if self.current_task != None:
            self.time_remaining = self.time_remaining - 1
            if self.time_remaining <= 0:
                self.current_task = None

    def busy(self):
        if self.current_task != None:
            return True
        return False

    def start_next(self, new_task):
        self.current_task = new_task
        self.time_remaining = new_task.get_pages() * 60 / self.pagerate


class Task:

    def __init__(self, time):
        self.timestamp = time
        self.pages = random.randrange(1, 21)

    def get_stamp(self):
        return self.timestamp

    def get_pages(self):
        return self.pages

    def wait_times(self, current_time):
        return current_time - self.timestamp


if __name__ == "__main__":
    for i in range(10):
        simulation(3600, 10)
