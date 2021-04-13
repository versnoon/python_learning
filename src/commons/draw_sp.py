#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   draw_sp.py
@Time    :   2021/04/13 13:35:59
@Author  :   Tong tan 
@Version :   1.0
@Contact :   tongtan@gmail.com
'''

import turtle


def draw_spiral(my_turtle, lin_len):
    if lin_len > 0:
        my_turtle.forward(lin_len)
        my_turtle.right(90)
        draw_spiral(my_turtle, lin_len - 5)


def tree(branch_len, t):
    if branch_len > 5:
        t.forward(branch_len)
        t.right(20)
        tree(branch_len - 15, t)
        t.left(40)
        tree(branch_len - 10, t)
        t.right(20)
        t.backward(branch_len)


if __name__ == "__main__":
    my_tur = turtle.Turtle()
    win = my_tur.getscreen()
    # draw_spiral(my_tur, 300)
    tree(110, my_tur)
    win.exitonclick()
