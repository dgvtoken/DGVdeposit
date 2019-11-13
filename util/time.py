#!/usr/bin/env python
# -*- coding:utf-8 -*
import datetime
import time
from datetime import datetime as dt, timezone

"""
This module work for time operation, if you need, you can add time operation in this file
"""

__datetime_formats = (
    '%Y-%m-%d %H:%M:%S',
    '%Y-%m-%d %H:%M:%S.%f',
    '%Y-%m-%d',
    '%H:%M:%S',
    '%H:%M:%S.%f',
    '%H:%M'
)

__date_parts__ = {'year', 'month', 'day', 'hour', 'minute', 'second'}

__date_trunc__ = {
    'year': '%Y',
    'month': '%Y-%m',
    'day': '%Y-%m-%d',
    'hour': '%Y-%m-%d %H',
    'minute': '%Y-%m-%d %H:%M',
    'second': '%Y-%m-%d %H:%M:%S'
}

# time stamp muliple
TIME_MULTIPLE = 1000

# current time stamp
now_time = int(round(time.time()) * TIME_MULTIPLE)


def format_date_time(value, formats, post_process=None):
    """
    这个函数会转化为日期型的的日期,如果不符合日期的转化格式会将原来的字符串类型的日期返回回来
    :param value: str 传入字符串的日期类型
    :param formats: list/tuple 需要转化成的日期格式
    :param post_process: function 转化完成之后需要进行的处理方式
    :return: <class 'datetime.datetime'> or str
    """
    post_process = post_process or (lambda x: x)
    for fmt in formats:
        try:
            return post_process(datetime.datetime.strptime(value, fmt))
        except ValueError:
            pass
    return value


def get_date_part(lookup_type, datetime_string):
    """
    这个函数用来获取格式化的日期的某个部分
    :param lookup_type: str 要获取到的部分的类型
    :param datetime_string: str 要处理的字符串的时间
    :return: str 返回相应的时间
    """
    assert lookup_type in __date_parts__
    if not datetime_string:
        return
    dt = format_date_time(datetime_string, __datetime_formats)
    return getattr(dt, lookup_type)


def get_date_trunc(lookup_type, datetime_string):
    """
    这个函数是用来获取日期的truncate
    :param lookup_type: str 要获取到的部分的类型
    :param datetime_string: str 要处理的字符串的时间
    :return: str 返回相应的时间(include pre time)
    """
    assert lookup_type in __date_trunc__
    if not datetime_string:
        return
    dt = format_date_time(datetime_string, __datetime_formats)
    return dt.strftime(__date_trunc__[lookup_type])


timeFormat = '%Y-%m-%dT%H:%M:%S'


def formatTime(t):
    """ Properly Format Time for permlinks
    """
    if isinstance(t, float):
        return dt.utcfromtimestamp(t).strftime(timeFormat)
    if isinstance(t, dt):
        return t.strftime(timeFormat)


def formatTimeString(t):
    """ Properly Format Time for permlinks
    """
    return dt.strptime(t, timeFormat)


def formatTimeFromNow(secs=0):
    """ Properly Format Time that is `x` seconds in the future

        :param int secs: Seconds to go in the future (`x>0`) or the
                         past (`x<0`)
        :return: Properly formated time for Graphene (`%Y-%m-%dT%H:%M:%S`)
        :rtype: str

    """
    return dt.utcfromtimestamp(
        time.time() + int(secs)).strftime(timeFormat)


def parse_time(block_time):
    """Take a string representation of time from the blockchain, and parse it
       into datetime object.
    """
    return dt.strptime(block_time, timeFormat).replace(
        tzinfo=timezone.utc)


# test
if __name__ == '__main__':
    res = format_date_time('2015-1-2 12:32:23', __datetime_formats)
    r = get_date_part('year', '2015-1-2 12:32:23')
    re = get_date_trunc('month', '2015-1-2 12:32:23')
    print(type(res))
    print(r)
    print(re)
    # r = formatTime(1524210699.4645011)
    # print(r)
    # r = formatTimeString('2018-04-20T07:51:39')
    r = formatTimeFromNow()
    print(r)