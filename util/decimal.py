#!/usr/bin/env python
# -*- coding:utf-8 -*

"""
这个模块可以使用内置的round来代替,但是round会有一些陷阱(https://blog.csdn.net/qq_28832135/article/details/79788757)
也可以使用Decimal来获取更精确的值
"""
from decimal import Decimal


def sub_decimal(target, point=5):
    """
    截取浮点数的小数位
    :param target: target float
    :param point: sub len
    :return: you want the float
    """
    try:
        target = str(Decimal(target))
        point_position = target.index('.')
        int_value = int(0) if point_position == int(0) else target[:point_position]
        float_value = float(target[point_position:point_position + point + 1])
        return int(int_value) + float_value
    except Exception as err:
        raise Exception('Money Format error. {}'.format(err))


if __name__ == "__main__":
    test = '342'
    sub_decimal(test, 5)
    print(sub_decimal(test, 5))
