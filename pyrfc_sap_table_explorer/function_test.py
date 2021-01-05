"""
功能测试
"""

import unittest
from SAP.table_info import SAPTableInfo

class TestTableExplorer(unittest.TestCase):

    def test_get_table_fields(self):
        sap = SAPTableInfo()
        fields = sap.get_table_fields("SPFLI")
        print(len(fields))
        for item in fields:
            print(item)

    def test_get_field_names(self):
        sap = SAPTableInfo()
        fieldnames = sap.get_field_names("SPFLI")
        print(len(fieldnames))
        for item in fieldnames:
            print(item)

    def test_get_field_contents(self):
        tablename = "SPFLI"
        sap = SAPTableInfo()
        fieldnames = sap.get_field_names(tablename)
        data = sap.get_table_contents(tablename, fieldnames[3:9], ",", 200)
        for item in data:
            print(item)

if __name__ == '__main__':
    unittest.main()
