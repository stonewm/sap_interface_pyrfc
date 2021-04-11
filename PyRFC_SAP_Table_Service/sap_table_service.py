from pyrfc import Connection
from pyrfc import ABAPApplicationError, ABAPRuntimeError, LogonError, CommunicationError
from configparser import ConfigParser
from collections import OrderedDict

COLS_PER_TIME = 5
MAX_ROWS = 200
ROWS_PER_TIME = 1000
CONFIG_FILE = "sapnwrfc.cfg"

def get_sap_logon_params(section_name):
    """
    get SAP logon parameters from sapnwrfc.cfg file
    """

    config = ConfigParser()
    config.read(CONFIG_FILE)

    # logon_params is of type OrderedDict
    logon_params = config._sections[section_name]

    return logon_params


class SapTableService(object):

    def __init__(self, systemid):
        """
        :param systemid: configured in sapnwrfc.cft file
        """

        self.systemid = systemid
        self.sap_connection = Connection(**get_sap_logon_params(systemid))

    def get_table_fields(self, table_name) -> list:
        """
        Get table structure via RFC_READ_ABLE function

        :param table_name: table name to query
        :return: table fields of type list[str]
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
        get all field names from table_name parameter

        :param table_name: table name
        :return: all fields in a table, which is of type list
        """
        fields = self.get_table_fields(table_name)
        field_names = map(lambda x: x.get("FIELDNAME"), fields)
        return list(field_names)

    def _get_table_contents(self, table_name, selected_fields, delimiter, rowcount, rowskips=0, where_options=''):
        options = list()
        options.append({"TEXT": where_options})

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

    def read_table(self, table_name, delimiter=',', rowcount=MAX_ROWS, rowskips=0, where_options='') -> list:
        """
        Get table data and returns a list of dict

        :param table_name: table name to be queried
        :param delimiter: delimiter will be used
        :param rowcount: row count of data output
        :param rowskips: row skips to select partial data
        :param where_options: filter criteria
        :return: list(dict) of DATA table paramter
        """

        rv = []        # method return value

        field_names = self._get_field_names(table_name)

        # -------------------------------------------------------------
        # Using 5 fieds at a time to avoid DATA_BUFFER_EXCEEDED error
        # -------------------------------------------------------------
        raw_data = []  # raw data returned from RF_READ_TABLE, needing further processing
        for idx in range(0, len(field_names), COLS_PER_TIME):
            selected_fields = field_names[idx: idx + COLS_PER_TIME]
            partial_data = self._get_table_contents(
                table_name, selected_fields, delimiter, rowcount, rowskips, where_options)

            # appending data to raw_data and keep track of the line number
            line_idx = 1  # line number
            for item in partial_data:
                raw_data.append({str(line_idx): item.get("WA")})
                line_idx += 1

        # -------------------------------------------------------------
        # Merge raw_data based on row number
        # -------------------------------------------------------------
        combined_lines = OrderedDict()
        for line in raw_data:
            for k, v in line.items():
                if k in combined_lines.keys():  # row number exists
                    combined_lines[k] = combined_lines[k] + delimiter + v # merge
                else: # row number does not exist
                    combined_lines[k] = v

        # -------------------------------------------------------------
        # Keep data and remove row numbers
        # -------------------------------------------------------------
        for k, v in combined_lines.items():
            rv.append(v)

        return rv

    def table_by_batch(self, table_name, rows_per_time, max_rows=MAX_ROWS, where_options=''):
        """
        Get table data by batch, rows fetched every time  equal rows_per_time，
        """

        row_skips = 0
        while True:
            result = self.read_table(
                table_name, rowcount=rows_per_time, rowskips=row_skips, where_options=where_options)

            row_skips += rows_per_time
            data_have_read = row_skips - rows_per_time
            if data_have_read > 0:
                print(f"{data_have_read} lines read ...")
            yield result

            if max_rows != -1 and row_skips >= max_rows:
                print(f"{max_rows} lines read successfully.")
                break

            if len(result) < rows_per_time:
                print(f"{data_have_read + len(result)} lines read successfully.")
                break

    def to_csv(self, table_name, **kwargs):
        """
        Export table data to csv file including header inforamtion

        :param table_name: SAP table name to be output
        :param kwargs:contains<br/>
            <b>file_name</b>: output file name<br/>
            <b>rows_per_time</b>: rows to be output each time<br/>
            <b>max_row</b>: default to 200 rows, -1 for all data<br/>
            <b>where_options</b>: criteria in open sql where clause, should be less than 72 characters<br/>
        :return: None
        """
        file_name = kwargs.setdefault("file_name", "output.csv")
        rows_per_time = kwargs.setdefault("rows_per_time", ROWS_PER_TIME)
        max_rows = kwargs.setdefault("max_rows", MAX_ROWS)
        where_options = kwargs.setdefault("where_options", '')

        with open(file_name, mode='a', encoding='utf8') as f:
            # write header
            f.write(",".join(self._get_field_names(table_name)) + "\n")

            # write table content
            for data in self.table_by_batch(table_name, rows_per_time, max_rows, where_options):
                for item in data:
                    f.write(item + '\n')
