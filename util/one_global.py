#!/usr/bin/env python
# -*- coding:utf-8 -*
from util.singleton import Singleton


class Global(Singleton):
    """
    这个类是提供全局变量的
    这个类的实现继承了单例模式类
    """
    def __init__(self):
        self.global_dict = {}

    def __getitem__(self, key, def_value=None):
        try:
            return self.global_dict[key]
        except KeyError:
            return def_value

    def __setitem__(self, key, value):
        self.global_dict[key] = value
