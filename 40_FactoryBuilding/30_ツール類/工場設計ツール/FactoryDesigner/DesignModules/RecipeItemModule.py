import os
import json


### 定数

# 配列のキー定数
RECIPE_NAME_KEY = "recipeName"
PRODUCT_NAME_KEY = "productName"
INPUT_KEY = "input"
OUTPUT_KEY = "output"
ITEM_NAME_KEY = "itemName"
ITEM_NUM_KEY = "itemNum"
SUPPLY_POWER_KEY = "supplyPower"


# 単一のレシピ
class RecipeItem:

    ### 変数 ###

    # Jsonファイル内のデータ
    jsonData = []

    
    # コンストラクタ
    def __init__(self,data):
        self.jsonData = data
        return


    # レシピ名
    def GetRecipeName(self) -> str:
        return self.jsonData[RECIPE_NAME_KEY]
    
    # 製造機器名
    def GetProductName(self) -> str:
        return self.jsonData[PRODUCT_NAME_KEY]
    
    
    # 加工元アイテムのリスト
    def GetInputItemList(self):
        return self.jsonData[INPUT_KEY]
    
    # 加工元アイテムのリスト長
    def GetInputItemLength(self):
        return len(self.GetInputItemList())
    
    # 加工元アイテムの名前
    def GetInputItemName(self,index):
        if index >= self.GetInputItemLength():
            return None
        return self.GetInputItemList(index)[ITEM_NAME_KEY]
    
    # 加工元アイテムの1分当たりの個数
    def GetInputItemNum(self,index):
        if index >= self.GetInputItemLength():
            return None
        return self.GetInputItemList(index)[ITEM_NUM_KEY]


    # 加工後アイテムのリスト
    def GetOutputItemList(self):
        if OUTPUT_KEY in self.jsonData:
            return self.jsonData[OUTPUT_KEY]
        return []
    
    # 加工後アイテムのリスト長
    def GetOutputItemLength(self):
        return len(self.GetOutputItemList())
    
    # 加工後アイテムの名前
    def GetOutputItemName(self,index):
        if index >= self.GetOutputItemLength():
            return None
        return self.GetOutputItemList(index)[ITEM_NAME_KEY]
    
    # 加工後アイテムの1分当たりの個数
    def GetOutputItemNum(self,index):
        if index >= self.GetOutputItemLength():
            return None
        return self.GetOutputItemList(index)[ITEM_NUM_KEY]
    
    # 供給電力を返す
    def GetSupplyPower(self):
        if SUPPLY_POWER_KEY in self.jsonData:
            return self.jsonData[SUPPLY_POWER_KEY]
        else:
            return 0
    
