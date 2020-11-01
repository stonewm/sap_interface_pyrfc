from SAP.sap_systems import get_sap_connection


class SAPGL(object):
    def __init__(self) -> None:
        self.sap_connection = get_sap_connection()

    def get_acc_balances(self, cocd, gl_account, fiscal_year):
        """
        获取会计科目在某一会计年度内按月份的发生额和余额
        """

        conn = self.sap_connection
        result = conn.call("BAPI_GL_ACC_GETPERIODBALANCES",
                           COMPANYCODE=cocd,
                           GLACCT=gl_account,
                           FISCALYEAR=fiscal_year,
                           CURRENCYTYPE="10")
        return result['ACCOUNT_BALANCES']

    def get_all_acc_balances(self, cocd, fiscal_year):
        """
        获取所有会计科目在某一会计年度内按月份的发生额和余额
        """

        # results for account balances
        gl_acc_balances = []

        # 获取所有会计科目
        accounts = self.get_gl_acc_list(cocd, '1')  # 1表示简体中文

        # 遍历会计科目，获取每一个科目的发生额和余额
        for item in accounts:
            account = item.get('GL_ACCOUNT')
            balances_in_year = self.get_acc_balances(cocd, account, fiscal_year)

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
