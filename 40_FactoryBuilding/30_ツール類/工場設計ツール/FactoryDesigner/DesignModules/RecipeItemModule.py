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


    # 値を返す
    def GetValue(self,key:str):
        if key in self.jsonData:
            return self.jsonData[key]
        return None

