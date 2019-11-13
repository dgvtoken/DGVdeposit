#!/usr/bin/env python  
# -*- coding: utf-8 -*-

import requests
import json

url = "https://open-api.eos.blockdog.com/v1/third/get_account_transfer"

headers = {
    'accept': "application/json;charset=UTF-8",
    'apikey': "49abe2e8-e598-415a-9239-e9244840674b",
    'content-type': "application/json"
}

payload = {
    "account_name": "dgvgoinggo11",
    # "code": "eosio.token",
    # "symbol": "EOS",
    "type": 1,
    "start_block_num": 1,
    "end_block_num": 200000000,
    "start_block_time": "2018-01-01T00:00:00",
    "end_block_time": "2030-01-01T00:00:00",
    "sort": 2,
    "size": 20,
    "page": 1
}

response = requests.post(url, data=json.dumps(payload), headers=headers)

print(response.text)
