#!/usr/bin/env python
# -*- coding:utf-8 -*
import time

from config.common_config import START, COUNT, SLEEP_STEP_TIMEOUT, TIME_MULTIPLE
from logs.log import Logger_record as Logger
from model.eos_db import EOSDbManage


def construct_deposit_record(record):
    time_stamp = int(round(time.time() * TIME_MULTIPLE))

    rec = dict()
    rec['out_trx_id'] = record['eos_trx_id']
    rec['eos_from_account'] = record['from_account']
    rec['like_d_account'] = record['user_id']
    rec['amount'] = record['amount']
    rec['asset_code'] = record['asset_code']
    rec['create_time'] = time_stamp
    rec['update_time'] = 0
    return rec


def construct_account_record(record):
    time_stamp = int(round(time.time() * TIME_MULTIPLE))

    rec = dict()
    rec['from_user_id'] = 0
    rec['to_user_id'] = record['user_id']
    rec['amount'] = record['amount']
    rec['asset_code'] = record['asset_code']
    rec['operation_type'] = 3
    rec['deposit_withdraw_id'] = record['id']
    rec['remark'] = record['eos_trx_id']
    rec['create_time'] = time_stamp
    rec['update_time'] = 0
    return rec


class DepositRecord(object):
    def __init__(self):
        super(DepositRecord, self).__init__()
        self.db = EOSDbManage()

    # 确认deposit请求记录
    def confirm_deposit_request(self, record_list):
        for record in record_list[::-1]:
            try:
                # 检查是否已经完成
                exist_record = self.db.select_deposit_record(record['eos_trx_id'])
                if exist_record:
                    Logger.error("Operate already, record:{}".format(record))
                    continue

                # 检查金额是否有效
                if record['amount'] <= 0:
                    Logger.error('amount is less than 0,from_account:{}, record:{}'.format(
                        record['from_account'], record))
                    continue

                self.transfer_and_record(record)
            except Exception as err:
                Logger.error('Confirm deposit request failed. record:{}, err:{}'.format(record, err))
                continue

    def transfer_and_record(self, record):
        try:
            new_deposit_record = construct_deposit_record(record)
            # 插入记录表
            self.db.insert_deposit_record(new_deposit_record)
            # 更新请求表中请求状态
            record['status'] = 'SUCCESS'
            self.db.update_deposit_request_status(record)
            self.db.update_account_balance(record)

            account_record = construct_account_record(record)
            self.db.insert_account_record(account_record)

            self.db.dbconn.commit()

            Logger.info(
                "transfer finish:account_name:{}, asset_code:{}, amount:{}".format(record['from_account'],
                                                                                   record['asset_code'],
                                                                                   record['amount']))
        except Exception as err:
            Logger.error('transfer_and_record failed. {}'.format(err))
            self.db.dbconn.rollback()
            try:
                record['status'] = 'FAIL'
                self.db.update_deposit_request_status(record)
                self.db.dbconn.commit()
            except Exception as err:
                self.db.dbconn.rollback()
                Logger.error('fail,  check log and program!!!!,uni_uuid:{}, error: {}'.format(record['uni_uuid'], err))

    def runloop(self):
        try:
            start = START
            page_size = COUNT

            while True:
                record_list = self.db.select_deposit_requests(start, page_size)

                count = len(record_list)
                if count <= 0:
                    start = 0
                    time.sleep(SLEEP_STEP_TIMEOUT)
                    continue

                self.confirm_deposit_request(record_list)
        except Exception as e:
            Logger.error('runloop failed. {}'.format(e))
