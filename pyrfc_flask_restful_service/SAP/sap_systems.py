import pyrfc

# 登录到SAP系统的参数
# Connect to D01 system
D01 = {
    "user": "stone",
    "passwd": "w123456",
    "ashost": "192.168.44.100",
    "sysnr": "00",
    "lang": "EN",
    "client": "001"
}


def get_sap_connection():
    logon_params = D01
    conn = pyrfc.Connection(**logon_params)

    return conn
