import pyrfc

# D01配置连接到D01系统
D01 = {
    "user": "stone",
    "passwd": "w123456",
    "ashost": "192.168.44.100",
    "sysnr": "00",
    "lang": "ZH",
    "client": "001"
}

def get_sap_connection(sap_logon_params):
    conn = pyrfc.Connection(**sap_logon_params)

    return conn


def current_sap_connection():
    return get_sap_connection(D01)
