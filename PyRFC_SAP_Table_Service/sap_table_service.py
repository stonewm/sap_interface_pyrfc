from pyrfc import Connection
from pyrfc import ABAPApplicationError, ABAPRuntimeError, LogonError, CommunicationError
from configparser import ConfigParser
from collections import OrderedDict

SECTION_NAME = "D01"
# SECTION_NAME = "DFQ"
COLS_AT_A_TIME = 5


def get_sap_logon_params(section_name):
    """
    从sapnwrfc.cfg文件获取SAP登录参数
    """

    config = ConfigParser()
    config.read('./.private/sapnwrfc.cfg')

    # logon_params is of type OrderedDict
    logon_params = config._sections[section_name]

    return logon_params


class SapTableService(object):

    def __init__(self):
        self.sap_connection = Connection(**get_sap_logon_params(SECTION_NAME))

    def get_table_fields(self, table_name) -> list:
        """
        通过 RFC_READ_TABLE 函数读取 SAP 表的字段结构

        :param table_name: table name to query
        :return: list[str]
        """

        rv = []
        try:
            result = self.sap_connection.call('RFC_READ_TABLE',
                                              QUERY_TABLE=table_name,
                                              NO_DATA="X")
            rv = result['FIELDS']
        except (CommunicationError, LogonError):
            raise

        return rv

    def _get_field_names(self, table_name) -> list:
        """
        返回 table 所有字段名(fieldname)

        :param table_name: table name
        :return: SAP表的所有字段，list类型
        """
        fields = self.get_table_fields(table_name)
        field_names = map(lambda x: x.get("FIELDNAME"), fields)
        return list(field_names)

    def _get_table_contents(self, table_name, selected_fields, delimiter, rowcount, rowskips=0, filter_criteria=''):
        options = list()
        options.append({"TEXT": filter_criteria})

        result = dict()
        try:
            result = self.sap_connection.call('RFC_READ_TABLE',
                                              QUERY_TABLE=table_name,
                                              DELIMITER=delimiter,
                                              FIELDS=selected_fields,
                                              ROWCOUNT=rowcount,
                                              ROWSKIPS=rowskips,
                                              OPTIONS=options)
        except CommunicationError:
            print("Could not connect to server.")
            raise
        except LogonError:
            print("Could not log in. Wrong credentials?")
            raise
        except (ABAPApplicationError, ABAPRuntimeError):
            print("An error occurred.")
            raise

        return result["DATA"]

    def read_table(self, table_name, delimiter=',', rowcount=200, rowskips=0, filter_criteria='') -> list:
        """
        读取SAP数据表的内容，返回list(dict)格式的数据

        :param table_name: table name to be queried
        :param delimiter: delimiter will be used
        :param rowcount: row count of data output
        :param rowskips: row skips to select partial data
        :param filter_criteria: filter criteria
        :return: list(dict) of DATA table paramter
        """

        rv = []  # 函数返回值
        raw_data = []  # 返回的DATA参数内容，每一行是delimiter字面量分割的字符串

        # 获取SAP table的所有字段名
        field_names = self._get_field_names(table_name)

        # 为避免 DATA_BUFFER_EXCEEDED 错误，每次选取其中5个字段
        for idx in range(0, len(field_names), COLS_AT_A_TIME):
            selected_fields = field_names[idx: idx + COLS_AT_A_TIME]
            # 每次获取部分字段的数据
            partial_data = self._get_table_contents(table_name, selected_fields, delimiter, rowcount, rowskips, filter_criteria)

            # 将数据整合在一起（纵向存放)
            line_idx = 1  # idx用于记录行号
            for item in partial_data:
                raw_data.append({str(line_idx): item.get("WA")})
                line_idx += 1

        # 上一步骤中line_idx标识了行号，依据line_idx将行数据横向合并
        combined_lines = OrderedDict()  # 存放按行合并的dict
        for line in raw_data:
            for k, v in line.items():
                if k in combined_lines.keys():  # 如果行号存在，表示该行已有数据，则合并
                    combined_lines[k] = combined_lines[k] + delimiter + v
                else:
                    combined_lines[k] = v

        # 去掉标识行号的key
        for k, v in combined_lines.items():
            rv.append(v)

        return rv

    def read_bybatch(self, table_name, rows_per_time, max_rows=10000):
        """
        分批获取SAP数据，每次获取行数为 rows_per_time，
        """
        row_skips = 0

        while True:
            result = self.read_table(table_name,rowcount=rows_per_time,rowskips=row_skips)
            print(f"{row_skips} lines read successfully...")
            row_skips += rows_per_time
            yield result

            if max_rows != -1 and row_skips >= max_rows:
                break
            if len(result) < rows_per_time:
                print(f"{row_skips + len(result)} lines read successfully.")
                break

    def to_csv(self, table_name, **kwargs):
        """
        将table_name的数据导出到csv文件，包含文件头

        :param table_name: SAP table name to be output
        :param kwargs:contains<br/>
            <b>file_name</b>: output file name<br/>
            <b>rows_per_time</b>: rows to be output each time<br/>
            <b>max_row</b>: default to 10,000, -1 for all data<br/>
        :return: None
        """
        kwargs.setdefault("file_name", "output.csv")
        kwargs.setdefault("rows_per_time", 1000)
        kwargs.setdefault("max_rows", 10000)

        with open(kwargs.get("file_name"), mode='a', encoding='utf8') as f:
            # header
            f.write(",".join(self._get_field_names(table_name)) + "\n")
            # content
            for data in self.read_bybatch(table_name, kwargs.get("rows_per_time"), kwargs.get("max_rows")):
                for item in data:
                    f.write(item + '\n')


