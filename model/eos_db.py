#!/usr/bin/env python
# -*- coding:utf-8 -*
import time

import pymysql

from config.common_config import gate_db_conn, TIME_MULTIPLE, chain_id
from logs.log import Logger
from util import globalvar as gl


class EOSDbManage(object):
    def __init__(self):
        gate_db_conn['password'] = gl.get_value('db_password')
        # gate_db_conn['password'] = 'root'
        self.dbconn = pymysql.connect(**gate_db_conn)

    def __del__(self):
        self.dbconn.close()

    def get_asset_code_from_basset(self, record):
        res = self.get_symbol_from_wasset(record['contract_address'], record['asset_code'], chain_id)

        record = None
        try:
            firstSQL = "SELECT asset_code FROM bitatom_asset WHERE " \
                       "base_symbol='%s' " % res['symbol']
            self.dbconn.connect()
            cursor = self.dbconn.cursor(pymysql.cursors.DictCursor)
            if cursor.execute(firstSQL) > 0:
                record = cursor.fetchone()
            cursor.close()
            return record
        except Exception as e:
            Logger.error('select_deposit_record failed. err:{}'.format(e))

    # todo
    def get_user_id_by_mobile(self, mobile):
        try:
            firstSQL = "SELECT user_id FROM dgv_user WHERE " \
                       "user_code_invite='%s' " % mobile
            self.dbconn.connect()
            cursor = self.dbconn.cursor(pymysql.cursors.DictCursor)
            record = None
            if cursor.execute(firstSQL) > 0:
                record = cursor.fetchone()
            cursor.close()
            return record
        except Exception as e:
            Logger.error('select_deposit_record failed. err:{}'.format(e))

    def update_last_block(self, keyword_id, end):
        """
            更新最后的充值区块
        :param keyword_id:
        :param end:
        :return:
        """
        current_time = int(round(time.time() * TIME_MULTIPLE))
        update_sql = "UPDATE deposit_block_stat_keyword SET keyword_value = {}, update_time = {} WHERE keyword_id = '{}' ".format(
            end, current_time, keyword_id)
        try:
            self.dbconn.connect()
            cursor = self.dbconn.cursor()
            cursor.execute(update_sql)
            self.dbconn.commit()
            cursor.close()
            # 返回影响的行数
            return format(cursor.rowcount)
        except Exception as e:
            self.dbconn.rollback()
            Logger.error('update_last_block fail. {}'.format(e))
            return 0

    def get_last_block(self, keyword_id):
        """
            获取最后的充值区块
        :param keyword_id:
        :return:
        """
        temp_row = None
        select_sql = "SELECT keyword_value FROM deposit_block_stat_keyword WHERE keyword_id = '{}'".format(
            keyword_id)
        try:
            self.dbconn.connect()
            cursor = self.dbconn.cursor(pymysql.cursors.DictCursor)
            cursor.execute(select_sql)
            temp_row = cursor.fetchone()
            cursor.close()
            return temp_row['keyword_value']
        except Exception as e:
            Logger.error('%s' % e)
        return temp_row

    def get_code_record(self, chain_id):
        """

        :return:
        """
        select_rows = None
        select_sql = "SELECT * FROM wallet_asset WHERE " \
                     "chain_id='%s' " % chain_id
        try:
            self.dbconn.connect()
            cursor = self.dbconn.cursor(pymysql.cursors.DictCursor)
            cursor.execute(select_sql)
            select_rows = cursor.fetchall()
            cursor.close()
        except Exception as err:
            Logger.error('Get code record failed. {}'.format(err))
        return select_rows

    def get_symbol_from_wasset(self, contract_account, asset_code, chain):
        record = None
        try:
            firstSQL = "SELECT symbol FROM wallet_asset WHERE " \
                       "display_symbol='%s' and contract_address='%s' and chain_id='%s' " % (
                       asset_code, contract_account, chain)
            self.dbconn.connect()
            cursor = self.dbconn.cursor(pymysql.cursors.DictCursor)
            if cursor.execute(firstSQL) > 0:
                record = cursor.fetchone()
            cursor.close()
            return record
        except Exception as e:
            Logger.error('select_deposit_record failed. err:{}'.format(e))

    # todo
    def exist_liked_account(self, account_name):
        select_rows = None
        select_sql = "SELECT mobile FROM dgv_user where user_code_invite='%s' " % account_name
        try:
            self.dbconn.connect()
            cursor = self.dbconn.cursor(pymysql.cursors.DictCursor)
            cursor.execute(select_sql)
            select_rows = cursor.fetchone()
            cursor.close()
        except Exception as err:
            Logger.error('exist_liked_account failed. {}'.format(err))
        return select_rows

    def exist_deposit_request(self, tx_id):
        select_rows = None
        select_sql = "SELECT id FROM dgv_deposit_request where eos_trx_id='%s' " % tx_id
        try:
            self.dbconn.connect()
            cursor = self.dbconn.cursor(pymysql.cursors.DictCursor)
            cursor.execute(select_sql)
            select_rows = cursor.fetchone()
            cursor.close()
        except Exception as err:
            Logger.error('exist_deposit_request failed. {}'.format(err))
        return select_rows

    def insert_deposit_request(self, rq):
        try:
            self.dbconn.connect()
            cursor = self.dbconn.cursor(pymysql.cursors.DictCursor)
            cursor.execute(
                "insert into dgv_deposit_request(eos_trx_id, from_account, to_account, user_id, amount, asset_code, block_num, deposit_status, create_time, update_time) values ('%s', '%s', '%s','%s', '%s', '%s', '%s',  '%s', '%s', '%s')" % (
                    rq['trx_id'], rq['from_account'],
                    rq['to_account'],
                    rq['like_d_account'], rq['amount'], rq['asset_code'],
                    rq['block_num'], rq['deposit_status'],
                    rq['create_time'], rq['update_time']))
            self.dbconn.commit()
            cursor.close()
        except Exception as e:
            self.dbconn.rollback()
            Logger.error('Insert in deposit request table failed. {}'.format(e))

    def select_deposit_requests(self, start, offset):
        record = {}
        try:
            sql = "SELECT * FROM dgv_deposit_request WHERE deposit_status ='INIT' " \
                  "order by `id` limit %s,%s" % (start, offset)
            self.dbconn.connect()
            cursor = self.dbconn.cursor(pymysql.cursors.DictCursor)
            if cursor.execute(sql) > 0:
                record = cursor.fetchall()
            cursor.close()
        except Exception as e:
            Logger.error('Query deposit request failed. {}'.format(e))
        return record

    def select_deposit_record(self, tx_id):
        record = None
        try:
            firstSQL = "SELECT * FROM dgv_deposit_record WHERE " \
                       "out_trx_id='%s' " % tx_id
            self.dbconn.connect()
            cursor = self.dbconn.cursor(pymysql.cursors.DictCursor)
            if cursor.execute(firstSQL) > 0:
                record = cursor.fetchone()
            cursor.close()
            return record
        except Exception as e:
            Logger.error('select_deposit_record failed. tx_id:{}, err:{}'.format(tx_id, e))

    def insert_deposit_record(self, record):
        try:
            cursor = self.dbconn.cursor(pymysql.cursors.DictCursor)

            secondSQL = "INSERT INTO dgv_deposit_record(out_trx_id, from_account, \
                                    user_id, amount,asset_code, create_time, update_time) " \
                        "VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (
                            record['out_trx_id'], record['eos_from_account'],
                            record['like_d_account'],
                            record['amount'], record['asset_code'], record['create_time'],
                            record['update_time'])
            cursor.execute(secondSQL)
        except Exception as err:
            Logger.error('insert_deposit_record failed. error:{}, record:{}'.format(err, record))

    def insert_account_record(self, record):
        try:
            cursor = self.dbconn.cursor(pymysql.cursors.DictCursor)

            secondSQL = "INSERT INTO dgv_account_record(from_user_id, to_user_id, \
                                    amount,asset_code, operation_type, deposit_withdraw_id,remark, create_time, update_time) " \
                        "VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (
                            record['from_user_id'], record['to_user_id'],
                            record['amount'],
                            record['asset_code'], record['operation_type'], record['deposit_withdraw_id'],
                            record['remark'],record['create_time'],record['update_time'])
            cursor.execute(secondSQL)
        except Exception as err:
            Logger.error('insert_account_record failed. error:{}, record:{}'.format(err, record))

    def update_account_balance(self, record):
        try:
            cursor = self.dbconn.cursor(pymysql.cursors.DictCursor)
            timeStamp = int(round(time.time() * TIME_MULTIPLE))
            thirdSQL = "update dgv_user_account set amount_available = amount_available+'%s', update_time = '%s' " \
                       "where user_id = '%s' and asset_code= '%s'" % (record['amount'], timeStamp, record['user_id'], record['asset_code'])
            cursor.execute(thirdSQL)
        except Exception as err:
            Logger.error('update_deposit_request_status failed. error:{}, record:{}'.format(err, record))

    def update_deposit_request_status(self, record):
        try:
            cursor = self.dbconn.cursor(pymysql.cursors.DictCursor)
            timeStamp = int(round(time.time() * TIME_MULTIPLE))
            thirdSQL = "update dgv_deposit_request set deposit_status = '%s', update_time = '%s' " \
                       "where eos_trx_id = '%s'" % (record['status'], timeStamp, record['eos_trx_id'])
            cursor.execute(thirdSQL)
        except Exception as err:
            Logger.error('update_deposit_request_status failed. error:{}, record:{}'.format(err, record))

# if __name__ == '__main__':
# keyword_id = 'last_eos_block_deposit'
# d = EOSDbManage()
# res = d.get_last_block(keyword_id)
# print(res)
# res = d.get_code_record()
# print(res)
