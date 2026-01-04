# 単一の設備情報
class BuildingDataItem:

    ### 定数

    # 配列のキー定数
    BUILDING_NAME_KEY = "buildingName"
    USE_POWER_KEY = "usePower"
    COST_KEY = "cost"

    ITEM_NAME_KEY = "itemName"
    ITEM_NUM_KEY = "itemNum"

    ### 変数 ###

    # Jsonファイル内のデータ
    jsonData = []

    
    # コンストラクタ
    def __init__(self,data):
        self.jsonData = data
        return


    # 設備名
    def GetBuildingName(self):
        return self.jsonData[self.BUILDING_NAME_KEY]
    
    # 消費電力
    def GetUsePower(self):
        return self.jsonData[self.USE_POWER_KEY]
    
    
    # 加工元アイテムのリスト
    def GetCostList(self):
        return self.jsonData[self.COST_KEY]
    
    # 加工元アイテムのリスト長
    def GetCostLength(self):
        return len(self.GetCostList())
    
    # 加工元アイテムの名前
    def GetCostName(self,index):
        if index >= self.GetCostLength():
            return None
        return self.GetCostList(index)[self.COST_KEY]
    
    # 加工元アイテムの1分当たりの個数
    def GetCostNum(self,index):
        if index >= self.GetCostLength():
            return None
        return self.GetCostList(index)[self.COST_KEY]
    
