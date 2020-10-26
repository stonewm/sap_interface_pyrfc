import pyrfc
import tablib

conn_params = {
    "user": "stone",
    "passwd": "w123456",
    "ashost": "192.168.44.100",
    "sysnr": "00",
    "lang": "EN",
    "client": "001"
}

def get_ac_balances(glaccount, fiscal_year):
    conn = pyrfc.Connection(**conn_params)

    result = conn.call("BAPI_GL_ACC_GETPERIODBALANCES", 
                        COMPANYCODE = "Z900",  
                        GLACCT = glaccount,
                        FISCALYEAR = fiscal_year,
                        CURRENCYTYPE = "10")   
    
    data = tablib.Dataset()
    data.dict = result['ACCOUNT_BALANCES']
    
    return data.json




