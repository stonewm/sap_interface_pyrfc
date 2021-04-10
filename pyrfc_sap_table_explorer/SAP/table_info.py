from SAP.sap_systems import current_sap_connection
from collections import OrderedDict

COLS_A_TIME = 5  # 单次读取的字段数量（column count a time）

class SAPTableInfo(object):
    def __init__(self):
        self.sap_connection = current_sap_connection()

    def read_table(self, tablename, delimiter='~', rowcount=200, filter_criteria='') -> list:
        """
        读取SAP数据表的内容，返回list(dict)格式的数据
        
        :param sap_tablename: table name to be queried
        :param delimiter: delimiter will be used
        :param rowcount: row count of data output
        :param options: filter criteria
        :return: list(dict) of DATA table paramter
        """
        rv = []  # 函数返回值
        raw_data = []  # 返回的DATA参数内容，每一行是delimiter字面量分割的字符串

        # 获取SAP table的所有字段名
        field_names = self.get_field_names(tablename)

        # 为避免 DATA_BUFFER_EXCEEDED 错误，每次选取其中5个字段
        for idx in range(0, len(field_names), COLS_A_TIME):
            selected_fields = field_names[idx: idx + COLS_A_TIME]
            # 每次获得的partial_table_data为SAP table部分字段的数据
            partial_data = self.get_table_contents(
                tablename, selected_fields, delimiter, rowcount, filter_criteria)

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

        # 因为每一行的数据是使用分隔符组合在一起的字符串，根据字段名还原成SAP表本来的样子
        for k, v in combined_lines.items():
            line_dict = OrderedDict()  # 存放每一行的数据
            line_values = v.split(delimiter)

            for idx, item in enumerate(field_names):
                line_dict[item] = line_values[idx]
            # for idx in range(len(field_names)):
            #     line_dict[field_names[idx]] = line_values[idx]

            rv.append(line_dict)

        return rv

    def get_field_names(self, table_name):
        """
        返回table所有字段名(fieldname)

        :param table_name: table name
        :return: SAP表的所有字段，list类型
        """
        fields = self.get_table_fields(table_name)
        field_names = []
        for item in fields:
            field_names.append(item.get('FIELDNAME'))

        return field_names

    def get_table_fields(self, table_name) -> list:
        """
        通过RFC_READ_TABLE读取SAP表的字段结构

        :param table_name: table name
        :return: list[str]
        """
        result = self.sap_connection.call('RFC_READ_TABLE',
                                          QUERY_TABLE=table_name,
                                          NO_DATA="X")

        return result['FIELDS']

    def get_table_contents(self, table_name, selected_fields, delimiter, rowcount, filter_criteria=''):
        options = list()
        options.append({"TEXT": filter_criteria})

        result = self.sap_connection.call('RFC_READ_TABLE',
                                          QUERY_TABLE=table_name,
                                          DELIMITER=delimiter,
                                          FIELDS=selected_fields,
                                          ROWCOUNT=rowcount,
                                          OPTIONS=options)

        return result["DATA"]
