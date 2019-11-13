#!/usr/bin/env python
# -*- coding:utf-8 -*

"""
This module work for tuple operation. If you need, you can add it.

"""


def ensure_tuple(value):
    if value:
        return value if isinstance(value, (list, tuple)) else (value,)
