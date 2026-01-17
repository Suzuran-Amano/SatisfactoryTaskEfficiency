### 定数 ###

# 配列のキー定数
BUILDING_NAME_KEY = "buildingName"
USE_POWER_KEY = "usePower"
COST_KEY = "cost"

ITEM_NAME_KEY = "itemName"
ITEM_NUM_KEY = "itemNum"

PRODUCTION_RATIO = "productionRatio"


# 単一の設備情報
class BuildingData:

    ### 変数 ###

    # Jsonファイル内のデータ
    jsonData = []

    
    # コンストラクタ
    def __init__(self,data):
        self.jsonData = data
        return
    
    # 値を返す
    def GetValue(self,key : str):
        if key in self.jsonData:
            return self.jsonData[key]
        return None

