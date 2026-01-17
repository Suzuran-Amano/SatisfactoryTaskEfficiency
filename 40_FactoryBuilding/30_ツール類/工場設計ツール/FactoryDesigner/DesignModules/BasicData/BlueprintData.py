### 定数

# 配列のキー定数
BLUEPRINT_NAME = "blueprintName"
DESCRIPTION = "description"
VERSION = "version"

# 設備情報
BUILDING_NAME = "buildingName"
COUNT = "count"

# 資材コスト
COST = "cost"
ITEM_NAME = "itemName"
AMOUNT = "amount"

# 電力情報
POWER = "power"
CONSUMPTION_MW = "consumptionMw"
PRODUCTION_MW = "productionMw"


# 単一のレシピ
class BlueprintData:

    ### 変数 ###

    # Jsonファイル内のデータ
    jsonData = []

    
    # コンストラクタ
    def __init__(self,data):
        self.jsonData = data
        return


    # 値を返す
    def GetValue(self,key:str):
        if key in self.jsonData:
            return self.jsonData[key]
        return None

