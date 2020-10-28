from SAP import sap_system
import pyrfc
import tablib

def get_ac_balances(cocd, glaccount, fiscal_year):
    logon_params = sap_system.conn_params
    conn = pyrfc.Connection(**logon_params)

    result = conn.call("BAPI_GL_ACC_GETPERIODBALANCES", 
                        COMPANYCODE = cocd,  
                        GLACCT = glaccount,
                        FISCALYEAR = fiscal_year,
                        CURRENCYTYPE = "10")   
    
    data = tablib.Dataset()
    data.dict = result['ACCOUNT_BALANCES']
    
    return data.json




