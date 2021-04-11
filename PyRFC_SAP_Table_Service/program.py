
from sap_table_service import SapTableService

if __name__ == '__main__':
    sap = SapTableService("D01")

    options = {
        "file_name": "output.csv",
        "rows_per_time": 20000,
        "max_rows": -1,
        "where_options": "SPRSL = '1' "
    }

    sap.to_csv("TSTCT", **options)