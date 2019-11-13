#!/usr/bin/ python3

import getpass
import sys
import time
from multiprocessing import Process

from config.common_config import ENCRYPT_KEY, TIME_MULTIPLE
from config.common_config import gate_db_conn as GATE_DB_CONN
from config.one_config import COIN_CONFIG
from core import deposit_record
from logs.log import Logger_record as Logger
from util import globalvar as gl
from util.one_encrypt import decrypt


def start():
    try:
        while True:
            monitor = deposit_record.DepositRecord()
            monitor.runloop()

            time.sleep(COIN_CONFIG.trans_period)  # 休眠指定时间后继续执行
    except Exception as er:
        Logger.error('Monitor run fail. {}'.format(er))


if __name__ == '__main__':
    try:
        input_passwd = getpass.getpass('Please input password:')
        key = input_passwd.strip()
        if key != decrypt(ENCRYPT_KEY, key).strip():
            Logger.info('Unlock password error')
            sys.exit(0)

        gl.init()
        gl.set_value('db_password', decrypt(GATE_DB_CONN['password'], key).strip())

    except Exception as err:
        Logger.error('Run start fail. {}'.format(err))
        sys.exit(0)

    Logger.info('RUN start time. {}'.format(int(round(time.time() * TIME_MULTIPLE))))

    process_list = list()
    p = Process(target=start, args=())  # 申请子进程
    process_list.append(p)

    # 启动所有进程
    for proc in process_list:
        proc.start()

    # 主线程中等待所有子进程退出
    for proc in process_list:
        proc.join()

    Logger.info("All process finished")
