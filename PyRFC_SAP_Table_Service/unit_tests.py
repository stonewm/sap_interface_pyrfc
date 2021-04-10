
import unittest
from sap_table_service import SapTableService
import pprint as pp

class TestSAPTableService(unittest.TestCase):
    
    def test_get_table_fields(self):
        sap = SapTableService()
        fields = sap.get_table_fields("T001")

        pp.pprint(fields)

    def test_get_field_names(self):
        sap = SapTableService()
        fields = sap._get_field_names("T001")

        pp.pprint(fields)

    def test_read_table(self):
        sap = SapTableService()
        data = sap.read_table("T001",delimiter=",",rowcount=20, rowskips=10)

        for item in data:
            print(item)

    def test_read_by_batch(self):
        sap = SapTableService()
        data = sap.read_bybatch("T001", 20)
        for item in data:
            print(item)

    def test_table_to_csv(self):
        sap = SapTableService()
        options = {
            "file_name": "output.csv",
            "rows_per_time" : 5000,
            "max_rows": -1
        }
        sap.to_csv("TSTCT", **options)


if __name__ == '__main__':
    unittest.main()