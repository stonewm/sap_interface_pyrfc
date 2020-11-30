from SAP.fixed_assets import FixedAsset
import pandas as pd

if __name__ == "__main__":
    # 从Excel读取数据
    asset_data = pd.read_excel("AS01_data.xlsx", sheet_name="Sheet1")

    fixedasset_obj = FixedAsset()

    # 遍历数据，每一行作为dict
    for indx, row in asset_data.iterrows():
        asset_info = {
            "asset_class": row["Asset Class"],
            "company_code": row["Company Code"],
            "description": row["Description"],
            "cost_center": row["Cost Center"]
        }

        # 创建固定资产
        rv = fixedasset_obj.create_asset(asset_info)
        print(rv)