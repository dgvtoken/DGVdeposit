#!/usr/bin/env python
# -*- coding:utf-8 -*
import copy
import json
import math
import time

import requests

from config.common_config import chain_id, SLEEP_STEP_TIMEOUT, TIME_MULTIPLE, \
    THIRD_PARTY_PAYLOAD, THIRD_PARTY_API, OFFICE_ACCOUNT, THIRD_PARTY_HEADERS
from core.common_function import get_liked_account_from_memo, filter_account
from core.common_function import get_office_account_count
from logs.log import Logger_request as Logger
from model.eos_db import EOSDbManage


class DepositRequest(object):

    def __init__(self):
        super(DepositRequest, self).__init__()
        self.db = EOSDbManage()

    def _op_code(self):
        code_list = self.db.get_code_record(chain_id)
        # code_list = list(filter(lambda x: x['chain'] == chain_id, code_list))
        contract_account = []
        asset_code = []
        for item in code_list:
            contract_account.append(item['contract_address'])
            asset_code.append(item['display_symbol'])
        return contract_account, asset_code

    @staticmethod
    def construct_request(tx_id, from_account, to_account, liked_account, amount, asset_code, block_num
                          ):
        rq = dict()
        rq['trx_id'] = tx_id
        rq['from_account'] = from_account
        rq['to_account'] = to_account
        rq['like_d_account'] = liked_account
        rq['amount'] = amount
        rq['asset_code'] = asset_code
        rq['block_num'] = block_num
        rq['deposit_status'] = 'INIT'
        rq['create_time'] = int(round(time.time()) * TIME_MULTIPLE)
        rq['update_time'] = 0
        return rq

    def process_deposit(self, tx_records):
        for tx in tx_records:
            try:
                tx_id = tx['id']
                block_num = tx['blockNum']
                amount, asset_code = tx['data']['quantity'].split(' ')
                # amount = tx['quantity']
                # asset_code = tx['symbol']
                from_account = tx['data']['from']
                to_account = tx['data']['to']
                memo = tx['data']['memo']
                if not memo.startswith('%') or not memo.endswith('%'):
                    Logger.warning('Deposit memo is not right. memo: {}'.format(tx['memo']))
                    continue

                liked_account = get_liked_account_from_memo(tx['data']['memo'])

                user_id_record = self.db.get_user_id_by_mobile(liked_account)
                if not user_id_record:
                    continue

                user_id = user_id_record['user_id']

                if not filter_account(liked_account) or not self.db.exist_liked_account(liked_account):
                    Logger.error('Memo account invalid.eos_acc:{}->one_acc:{}'.format(from_account, liked_account))
                    continue

                if to_account != OFFICE_ACCOUNT:
                    Logger.error('office account error. to_account:{}'.format(to_account))
                    continue

                if from_account.startswith('eosio.'):
                    Logger.info('system transfer not op. account: {}'.format(from_account))
                    continue

                c_request = self.construct_request(tx_id,
                                                   from_account,
                                                   to_account,
                                                   user_id,
                                                   amount,
                                                   asset_code,
                                                   block_num,
                                                   )

                if self.db.exist_deposit_request(tx_id):
                    Logger.info('Deposit request exist. c_request: {}'.format(c_request))
                    continue
                self.db.insert_deposit_request(c_request)

            except Exception as err:
                Logger.error('process_deposit failed. tx:{}, err:{}'.format(tx, err))

    @staticmethod
    def get_trx_records(api_params):
        res_obj = requests.post(THIRD_PARTY_API, data=json.dumps(api_params), headers=THIRD_PARTY_HEADERS)
        res = json.loads(res_obj.text)
        if hasattr(res, 'error'):
            err_count = 0
            while err_count < 3:
                res_obj = requests.post(THIRD_PARTY_API, data=json.dumps(api_params), headers=THIRD_PARTY_HEADERS)
                res = json.loads(res_obj.text)
                if res['total'] > 0:
                    break
                else:
                    err_count += 1
            if res['error']:
                raise Exception('Repeat call page-{} api error.'.format(api_params['page']))
            else:
                return res['list']
        else:
            return res['list']

    def runloop(self):
        try:
            while True:
                office_account_receive_count = get_office_account_count()
                if office_account_receive_count > 0:
                    page = int(math.ceil(office_account_receive_count / THIRD_PARTY_PAYLOAD['size']))
                    new_payload = copy.deepcopy(THIRD_PARTY_PAYLOAD)
                    for page_item in range(1, page + 1):
                        try:
                            new_payload['page'] = page_item
                            trx_records = self.get_trx_records(new_payload)
                            for index, value in enumerate(trx_records):
                                if value['account'] not in ["eosio.token", "dgvtoken1533"]:
                                    del trx_records[index]
                            self.process_deposit(trx_records)
                        except Exception as e:
                            Logger.error(
                                "Get page item content fail. "
                                "err: {}, page: {}, office_account: {}".format(e, page_item,
                                                                               new_payload[
                                                                                   'account_name']))
                        finally:
                            time.sleep(SLEEP_STEP_TIMEOUT)
                else:
                    time.sleep(SLEEP_STEP_TIMEOUT)
                    continue

        except Exception as err:
            Logger.error('Runloop failed. {}'.format(err))
