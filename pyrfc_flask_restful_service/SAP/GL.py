from SAP import sap_system
import pyrfc

def get_sap_connection():
    logon_params = sap_system.sap_conn_params
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
        return result['ACCOUNT_BALANCES']

    def get_all_acc_balances(self, cocd, fiscal_year):
        """
        获取所有会计科目在某一会计年度内按月份的发生额和余额
        """

        # results for account balances
        gl_acc_balances = []

        accounts = self.get_gl_acc_list(cocd, '1')

        # 获取所有会计科目
        gl_account_list = []
        for item in accounts:
            gl_account_list.append(item.get('GL_ACCOUNT'))

        # 遍历会计科目，获取每一个科目的发生额和余额
        for glacc in gl_account_list:
            balances_in_year = self.get_ac_balances(cocd, glacc, fiscal_year)

            for period_balance in balances_in_year:
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
        return result['ACCOUNT_LIST']
