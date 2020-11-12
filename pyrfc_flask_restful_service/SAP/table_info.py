from SAP.sap_systems import current_sap_connection
from collections import OrderedDict

BATCH_COL_COUNT = 5  # 单次读取的字段数量（batch column count）


class SAPTableInfo(object):
    def __init__(self):
        self.sap_connection = current_sap_connection()

    def read_table(self, sap_tablename, delimiter='~', rowcount=200) -> list:
        """
        读取SAP数据表的内容，返回list(dict)格式的数据
        :param sap_tablename: table name to be queried
        :param delimiter: delimiter will be used
        :param rowcount: row count of data output
        :return: list(dict) of DATA table paramter
        """
        rv = []  # 函数返回值
        raw_data_returned = []  # 返回的DATA参数内容，每一行是delimiter字面量分割的字符串

        # 获取SAP table的所有字段名
        field_names = self.get_field_names(sap_tablename)

        # 为避免 DATA_BUFFER_EXCEEDED 错误，每次读取其中5个字段并获取这些字段的值
        for idx in range(0, len(field_names), BATCH_COL_COUNT):
            batch_fields = field_names[idx: idx + BATCH_COL_COUNT]
            # 每次获得的partial_table_data为SAP table部分字段的数据
            batch_fields_data = self.get_table_contents(sap_tablename, batch_fields, delimiter, rowcount)

            # 将数据整合在一起（纵向存放)
            line_idx = 1  # idx用于记录行号
            for item in batch_fields_data:
                raw_data_returned.append({str(line_idx): item.get("WA")})
                line_idx += 1

        # 上一步骤中line_idx标识了行号，依据line_idx将行数据横向合并
        combined_lines = OrderedDict()  # 存放按行合并的dict
        for line in raw_data_returned:
            for k, v in line.items():
                if k in combined_lines.keys():  # 如果行号存在，表示该行已有数据，则合并
                    combined_lines[k] = combined_lines[k] + delimiter + v
                else:
                    combined_lines[k] = v

        # 因为每一行的数据是使用分隔符组合在一起的字符串，根据字段名还原成SAP表本来的样子
        for k, v in combined_lines.items():
            line_dict = OrderedDict()  # 存放每一行的数据
            line_values = v.split(delimiter)

            for idx in range(len(field_names)):
                line_dict[field_names[idx]] = line_values[idx]

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
        :return: list[dict]
        """
        result = self.sap_connection.call('RFC_READ_TABLE',
                                          QUERY_TABLE=table_name,
                                          NO_DATA="X")

        return result['FIELDS']

    def get_table_contents(self, table_name, selected_fields, delimiter, rowcount):
        result = self.sap_connection.call('RFC_READ_TABLE',
                                          QUERY_TABLE=table_name,
                                          DELIMITER=delimiter,
                                          FIELDS=selected_fields,
                                          ROWCOUNT=rowcount)

        return result["DATA"]
