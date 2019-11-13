#!/usr/bin/env python
# -*- coding:utf-8 -*

"""this module work for constants define to promise the code work better."""
from collections import namedtuple


def declare_constants(**name_value_dict):
    """this function work for declare constants"""
    ConstantContainer = namedtuple(
        'ConstantContainer',
        name_value_dict.keys()
    )
    return ConstantContainer(*name_value_dict.values())
