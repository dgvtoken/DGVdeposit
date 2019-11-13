#!/usr/bin/env python
# -*- coding:utf-8 -*
import json

import requests

from config.common_config import TX_URL
from config.common_config import cmd
from config.common_config import THIRD_PARTY_PAYLOAD, THIRD_PARTY_API, THIRD_PARTY_HEADERS
from config.eos_config import memo_keyword
from logs.log import Logger


def get_office_account_count():
    count = 0
    try:
        res_obj = requests.post(THIRD_PARTY_API, data=json.dumps(THIRD_PARTY_PAYLOAD), headers=THIRD_PARTY_HEADERS)
        res = json.loads(res_obj.text)
        if hasattr(res, 'error'):
            Logger.error("Call third api fial. error: {}".format(res['error']))
        else:
            count = res['total']
    except Exception as e:
        Logger.error("Get office account trx count fails. error: {}".format(e))
    finally:
        return count


# def check_onechain_account(name):
#     return ws.get_account(name)


def get_transactions_deposit(start,
                             offset,
                             to_name,
                             from_name,
                             contract_name,
                             symbol_name):
    """

    example:
        {"symbols": [{"symbolName": "EOS", "contractName": "eosio.token"}], "from": "xxx", "to": "", "page": 0,
     "pageSize": 30}
    :param offset:
    :param from_name:
    :param to_name:
    :param start:
    :param contract_name:
    :param symbol_name:
    :return:
    """
    assert isinstance(contract_name, list)
    assert isinstance(symbol_name, list)

    def construct_dict(args):
        data = dict()
        data['symbolName'] = args[0]
        data['contractName'] = args[1]
        return data

    post_dict = dict()
    post_dict['symbols'] = list(map(construct_dict, zip(symbol_name, contract_name)))
    post_dict['from'] = from_name
    post_dict['to'] = to_name
    post_dict['page'] = start
    post_dict['pageSize'] = offset

    data = json.dumps(post_dict)
    headers = {'content-type': 'application/json'}
    res = requests.post(TX_URL, data=data, headers=headers)
    return json.loads(res.text)


def get_liked_account_from_memo(memo):
    """
    memo:  %{name}%

    :param memo:str
    :return:
    """

    # NOTE: these code can't change: ` "" if not memo else str(memo) `

    return '' if not memo else memo.strip('a')


def filter_account(name):
    if name in memo_keyword:
        Logger.error('Invalid account name.')
        return False
    return True

# if __name__ == '__main__':
# wsapi = connect_ws('ws://47.92.108.254:31201')
# res = wsapi.get_account('one')
# print(res)
# res = get_transactions_deposit(5, 10, 'deposit11111', '', ['eosio.token'], ['SBC'])
# print(res)
# memo = str({"f8": "{\"cmd\":\"deposit\",\"memo\":\"xggh\"}"})
# memo = 'afd'
# res = get_one_account_from_memo(memo)
# print(res)
# memo = str({"f8":"{\"cmd\":\"deposit\",\"memo\":""}"})
# res = get_one_account_from_memo(memo)
# print(res)
