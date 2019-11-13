#!/usr/bin/env python
# -*- coding:utf-8 -*

gate_db_conn = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': b'\xd0\xf8lr\x14\x9c\xa6\xcf\x190-\xc7\xe7\xd0\x00\xd8_\xbb"_\x81]V\xc85\xae\x10\xe4*M\xdb\xc9',
    'db': 'dgv'
}

# time stamp muliple
TIME_MULTIPLE = 1000

# the private_key
ENCRYPT_KEY = b'3\xc4\x8c"\xe2\xbb\x82\x12["\xb5\x1b\xa6+\xb9n'

PAGE_START = 0

PAGE_SIZE = 1

last_block_num = 'last_eos_block_deposit'

SLEEP_STEP_TIMEOUT = 5

SLEEP_TIME_REQUEST = 30

TX_URL = 'http://222.180.164.141:18080/VX/GetActions'
# TX_URL = 'http://222.180.164.130:18080/VX/GetActions'

chain_id = 'aca376f206b8fc25a6ed44dbdc66547c36c6c33e3a119ffbeaef943642f0e906'

cmd = 'deposit'

START = 0

COUNT = 10

OFFICE_ACCOUNT = "dgvgoinggo11"

# https://developer.eospark.com/api-doc/zh/https/account.html#get-account-related-trx-info
# THIRD_PARTY_API = "https://api.eospark.com/api"
# THIRD_PARTY_PAYLOAD = {
#     "apikey": "74437f51b9543df893a4ab7f2673f01f",
#     "module": "account",
#     "action": "get_account_related_trx_info",
#     "account": OFFICE_ACCOUNT,
#     "symbol": "EOS",
#     "transaction_type": 1,
#     "sort": 2,
#     "code": "eosio.token",
#     "page": 1,
#     "size": 20
# }
THIRD_PARTY_API = "https://open-api.eos.blockdog.com/v1/third/get_account_transfer"

THIRD_PARTY_HEADERS = {
    'accept': "application/json;charset=UTF-8",
    'apikey': "********",
    'content-type': "application/json"
}

THIRD_PARTY_PAYLOAD = {
    "account_name": OFFICE_ACCOUNT,
    # "code": "eosio.token",
    # "symbol": "EOS",
    "type": 1,
    "start_block_num": 1,
    "end_block_num": 300000000,
    "start_block_time": "2018-01-01T00:00:00",
    "end_block_time": "2030-01-01T00:00:00",
    "sort": 2,
    "size": 20,
    "page": 1
}
