#!/usr/bin/env python
# -*- coding:utf-8 -*
from util.constants import declare_constants

coin_config = {
    'url': '***',  # RPC connection settings
    'user': '',
    'password': '',
    'account_name': "****",
    'account_id': "***8",  # Account id to monitor
    'memo_wif_key': b'\x03\xe2\x03\xa03\xce\xf2\xf8D^\x92K&\x9b]_RFl<\x03\xcb\xe7W\xabx\xb0k8\x82\xf9lP\x94@\xe4X{dT\x93\x03\xd9\xbb<9\xc0\xd8\xba\x11\x1f\xcf\xec\xc2o\x91\x15\xa8r(\x9c>$:',
    'last_op': "1.11.0",  # Last operation ID that you have registered in your backend
    'trans_period': 10,
    'nobroadcast': False  # Safety mode
}

COIN_CONFIG = declare_constants(**coin_config)
