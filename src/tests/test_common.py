#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   test_common.py
@Time    :   2021/03/17 16:36:39
@Author  :   Tong tan
@Version :   1.0
@Contact :   tongtan@gmail.com
'''


from collections.abc import Iterator, Iterable
import functools
import types


def log(func):
    def wrapper(*args, **kw):
        print('call %s ():' % func.__name__)
        return func(*args, **kw)
    return wrapper


def log_txt(msg: str):

    def log_dec(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            """
                log_txt
            """
            print('call %s %s()' % (msg, func.__name__))
            return func(*args, **kw)
        return wrapper
    return log_dec


class TestCommon:

    def test_arr_creator(self):
        arr = [x * x for x in range(1, 10)]
        assert len(arr) == 9
        assert arr[0] == 1
        assert arr[1] == 4
        assert arr[8] == 9 * 9

        arr_1 = [s.lower() if isinstance(s, str) else s for s in range(1, 10)]
        assert len(arr_1) == 9
        assert arr_1[8] == 9

        # 凡是可作用于next()函数的对象都是Iterator类型，它们表示一个惰性计算的序列
        assert isinstance(arr_1, Iterator) == False
        assert isinstance(iter(arr_1), Iterator)
        assert isinstance(arr_1, Iterable)  # 凡是可作用于for循环的对象都是Iterable类型

    @log_txt('exc')
    def count(self):
        fs = []
        for i in range(1, 4):
            def f():
                return i*i
            fs.append(f)
        return fs

    @log_txt("hello ")
    def print_log(self, m: str):
        """
        print_log
        """
        print(m)


if __name__ == "__main__":
    t = TestCommon()
    f1, f2, f3 = t.count()
    print(f1())
    print(f2())

    f = t.print_log
    f("tt")
    print(f.__name__)
    print(f.__doc__)
    print(type(t))
    print(type(f))
    print(type(12))
    print(type(12.))
    print(type("12."))
    print(dir(t))
    print(dir(f))
    assert types.FunctionType == type(f)
