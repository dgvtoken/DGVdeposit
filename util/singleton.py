#!/usr/bin/env python
# -*- coding:utf-8 -*

"""这个类是实现单例模式,如果你需要实现一个单例模式的类可以继承这个类来实现"""


class Singleton(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance
