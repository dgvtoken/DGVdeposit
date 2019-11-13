#!/usr/bin/env python
# -*- coding:utf-8 -*
import json


def check_json_format(input_str):
    """
    用于判断一个字符串是否符合Json格式
    """
    if isinstance(input_str, str):  # 首先判断变量是否为字符串
        try:
            json.loads(input_str, encoding='utf-8')
        except ValueError:
            return False
        return True
    else:
        return False


def check_json_simple(input_str):
    try:
        json.loads(input_str)
        return True
    except Exception as e:
        return False
