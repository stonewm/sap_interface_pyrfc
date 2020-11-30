from SAP.sap_systems import current_sap_connection


class FixedAsset(object):
    def __init__(self) -> None:
        self.sap_connection = current_sap_connection()

    def create_asset(self, asset_info):
        conn = self.sap_connection
        result = conn.call('ZFM_AS01',
                           ANLKL=asset_info['asset_class'],
                           BUKRS=asset_info['company_code'],
                           NASSETS="1",
                           TXT50=asset_info['description'],
                           MEINS="EA",
                           KOSTL=asset_info['cost_center']
                           )  
        
        # 选取三个最重要的字段返回
        raw_return = result['MESSTAB']        
        return_info = []
        for item in raw_return:
            line =  {
                "message type": item["MSGTYP"],
                "message number": item["MSGID"] + item["MSGNR"],
                "message": item["MSGV1"]
            }
            return_info.append(line)
            
        return return_info
