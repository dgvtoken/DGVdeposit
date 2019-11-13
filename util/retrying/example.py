#!/usr/bin/env python
# -*- coding:utf-8 -*
import random
from tenacity import retry

"""
example: http://tenacity.readthedocs.io/en/latest/
"""
@retry
def never_give_up_never_surrender():
    print("Retry forever ignoring Exceptions, don't wait between retries")
    raise Exception