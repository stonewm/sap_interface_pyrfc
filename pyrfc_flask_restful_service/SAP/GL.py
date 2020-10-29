from SAP import sap_system
import pyrfc
import tablib
import json


def get_sap_connection():
    logon_params = sap_system.conn_params
    conn = pyrfc.Connection(**logon_params)

    return conn


class SAPGL(object):
    def __init__(self) -> None:
        self.sap_connection = get_sap_connection()

    def get_ac_balances(self, cocd, g_laccount, fiscal_year):
        """
        获取会计科目在某一会计年度内按月份的发生额和余额
        """

        conn = self.sap_connection

        result = conn.call("BAPI_GL_ACC_GETPERIODBALANCES",
                           COMPANYCODE=cocd,
                           GLACCT=g_laccount,
                           FISCALYEAR=fiscal_year,
                           CURRENCYTYPE="10")

        data = tablib.Dataset()
        data.dict = result['ACCOUNT_BALANCES']

        return data.json

    def get_all_acc_balances(self, cocd, fiscal_year):
        """
        获取所有会计科目在某一会计年度内按月份的发生额和余额
        """

        # result list for account balances
        gl_acc_balances = []

        accounts = self.get_gl_acc_list(cocd, '1')
        data = tablib.Dataset()
        data.json = accounts

        gl_account_list = []
        for item in data.dict:
            gl_account_list.append(item.get('GL_ACCOUNT'))

        for glacc in gl_account_list:
            yearly_balances = json.loads(self.get_ac_balances(cocd, glacc, fiscal_year))

            for period_balance in yearly_balances:
                gl_acc_balances.append(period_balance)

        return gl_acc_balances

    def get_gl_acc_list(self, cocd, lang):
        """
        获取会计科目清单
        """

        conn = self.sap_connection

        result = conn.call("BAPI_GL_ACC_GETLIST",
                           COMPANYCODE=cocd,
                           LANGUAGE=lang)

        data = tablib.Dataset()
        data.dict = result['ACCOUNT_LIST']

        return data.json
