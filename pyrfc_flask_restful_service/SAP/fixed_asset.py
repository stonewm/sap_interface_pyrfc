from SAP.sap_systems import current_sap_connection


class FixedAsset(object):
    def __init__(self) -> None:
        self.sap_connection = current_sap_connection()

    def test_create_asset(self):
        asset_info = {
            "key": {
                "COMPANYCODE": "Z900"
            },
            "general_data": {
                "ASSETCLASS": "Z060",
                "DESCRIPT": "数据备份软件1"
            },
            "general_data_x": {
                "ASSETCLASS": "X",
                "DESCRIPT": "X"
            },
            "time_dependent_data": {
                "COSTCENTER": "Z90020"
            },
            "time_dependent_data_x": {
                "COSTCENTER": "X"
            },
            "depreciation_data": [
                {
                    "AREA": "01",
                    "DEP_KEY": "Z002",
                    "ULIFE_YRS": "3",
                    "ULIFE_PRDS": "0"
                },
                {
                    "AREA": "20",
                    "DEP_KEY": "Z002",
                    "ULIFE_YRS": "3",
                    "ULIFE_PRDS": "0"
                }],
            "depreciation_data_x": [{
                "AREA": "01",
                "DEP_KEY": "X",
                "ULIFE_YRS": "X",
                "ULIFE_PRDS": "X"
            },
                {
                "AREA": "20",
                "DEP_KEY": "X",
                "ULIFE_YRS": "X",
                "ULIFE_PRDS": "X"
            }]
        }

        conn = self.sap_connection
        result = conn.call('BAPI_FIXEDASSET_CREATE1',
                           KEY=asset_info["key"],
                           GENERALDATA=asset_info["general_data"],
                           GENERALDATAX=asset_info["general_data_x"],
                           TIMEDEPENDENTDATA=asset_info["time_dependent_data"],
                           TIMEDEPENDENTDATAX=asset_info["time_dependent_data_x"],
                           DEPRECIATIONAREAS=asset_info["depreciation_data"],
                           DEPRECIATIONAREASX=asset_info["depreciation_data_x"])

        if result['ASSET'] == None:
            conn.call('BAPI_TRANSACTION_ROLLBACK')
        else:
            conn.call('BAPI_TRANSACTION_COMMIT')

        return result['RETURN']

    def create_asset(self, asset_info):
        conn = self.sap_connection
        result = conn.call('BAPI_FIXEDASSET_CREATE1',
                           KEY=asset_info['key'],
                           GENERALDATA=asset_info['general_data'],
                           GENERALDATAX=asset_info['general_data_x'],
                           TIMEDEPENDENTDATA=asset_info['time_dependent_data'],
                           TIMEDEPENDENTDATAX=asset_info['time_dependent_data_x']
                           )
        if result['ASSET'] == None:
            conn.call('BAPI_TRANSACTION_ROLLBACK')
        else:
            conn.call('BAPI_TRANSACTION_COMMIT')

        return result['RETURN']
