
from pyrfc import Connection
from pyrfc import ABAPApplicationError, ABAPRuntimeError, LogonError, CommunicationError
from configparser import ConfigParser


def get_sap_logon_params():
    """
    从sapnwrfc.cfg文件获取SAP登录参数
    """

    config = ConfigParser()
    config.read('sapnwrfc.cfg')

    # logon_params is of type OrderedDict
    logon_params = config._sections['D01']

    return logon_params


def get_data_by_batch(batch_count):
    """
    分批获取SAP数据，batch_count作为RFC_READ_TABLE的rowcount，
    rowskips也依据该参数变化
    """
    ROWS_AT_A_TIME = batch_count
    row_skips = 0

    try:
        logon_params = get_sap_logon_params()
        sapconn = Connection(**logon_params)

        while True:
            result = sapconn.call('RFC_READ_TABLE',
                                  QUERY_TABLE='TSTCT',
                                  DELIMITER=',',
                                  ROWSKIPS=row_skips,
                                  ROWCOUNT=ROWS_AT_A_TIME)

            print(row_skips)
            row_skips += ROWS_AT_A_TIME            
            yield result["DATA"]
            if len(result['DATA']) < ROWS_AT_A_TIME:
                break
    except CommunicationError:
        print("Could not connect to server.")
        raise
    except LogonError:
        print("Could not log in. Wrong credentials?")
        raise
    except (ABAPApplicationError, ABAPRuntimeError):
        print("An error occurred.")
        raise


if __name__ == '__main__':

    with open('output.csv', mode='a', encoding='utf8') as f:
        for data in get_data_by_batch(1000):
            for item in data:
                f.write(item['WA'] + '\n')

    print("Done!")
