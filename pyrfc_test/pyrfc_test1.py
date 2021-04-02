import pyrfc
import tablib

conn_params = {
    "user": "stone",
    "passwd": "w123456",
    "ashost": "sapecc6",
    "sysnr": "00",
    "lang": "EN",
    "client": "001"
}


def dest_connection():
    conn = pyrfc.Connection(**conn_params)
    result = conn.call("STFC_CONNECTION", REQUTEXT="hello SAP")

    print(result["ECHOTEXT"])


def get_cocd_detail():
    conn = pyrfc.Connection(**conn_params)
    result = conn.call("BAPI_COMPANYCODE_GETDETAIL", COMPANYCODEID='Z900')

    ds = tablib.Dataset()
    ds.dict = result['COMPANYCODE_ADDRESS']
    print(ds)


def read_table():
    conn = pyrfc.Connection(**conn_params)

    option_parameter = [
        {"TEXT": "COUNTRYFR EQ 'US' "}
    ]

    result = conn.call('RFC_READ_TABLE', 
                        QUERY_TABLE = "SPFLI",  
                        DELIMITER = ",",
                        OPTIONS = option_parameter)

    # 获取 FIELDS 表参数
    fields = tablib.Dataset()
    fields.dict = result['FIELDS']
    print(fields)

    # 获取 DATA 标参数
    data = tablib.Dataset()
    data.dict = result['DATA']
    print(data)    


if __name__ == "__main__":
    read_table()
