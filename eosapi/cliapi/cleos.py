# -*- coding:utf-8 -*-

import subprocess
from config.eos_config import *
from decimal import Decimal


class Cleos():

    """
    EOS相关操作类
    """

    def __init__(self, agent=agent,
                 basePath=basePath, walletUrl=walletUrl,
                 walletPwd=walletPwd, nodeUrl=nodeUrl):
        self.agent = agent
        self.basePath = basePath
        self.walletUrl = walletUrl
        self.walletPwd = walletPwd
        self.nodeUrl = nodeUrl

    def exec(self, cmd=None):
        childPs = subprocess.Popen(cmd, shell=True)
        out = childPs.communicate()[0]
        if out:
            return str(out)
        else:
            return None

    def openWallet(self):
        cmd = self.basePath + ' --wallet_url ' + self.walletUrl + ' -url ' + self.nodeUrl + ' wallet unlock -n default ' \
              '--password ' + self.walletPwd
        out = self.exec(cmd=cmd)
        return out

    def transfer(self, to, amount, memo):
        assert amount > 0
        cmd = self.basePath + ' --wallet_url ' + self.walletUrl + ' -url ' + self.nodeUrl + ' transfer ' + self.agent + \
              ' ' + to + amount + ' "' + memo + '"'
        out = self.exec(cmd)
        return out

    def getHistory(self, account, position=0, offset=10):
        cmd = self.basePath + ' --wallet_url ' + self.walletUrl + ' -url ' + self.nodeUrl + ' get actions ' + account + \
              ' ' + position + ' ' + offset
        out = self.exec(cmd)
        return out

    def getBlock(self, block_num_or_id):
        cmd = self.basePath + ' get block ' + block_num_or_id
        out = self.exec(cmd)
        return out

    def moneyFormat(self, money):
        assert money > 0
        money = Decimal(money)
        return money