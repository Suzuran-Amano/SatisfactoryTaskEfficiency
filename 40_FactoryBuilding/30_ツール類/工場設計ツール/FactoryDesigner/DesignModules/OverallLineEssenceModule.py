import json

### 定数 ###
FACTORY_NAME_KEY = "factoryName"

RECIPE_LIST_KEY = "recipeList"
RECIPE_NAME_KEY = "recipeName"
RECIPE_NUM_KEY = "recipeNum"

INPUT_LINE_LIST = "inputlLineList"
OUTPUT_LINE_LIST = "outputLineList"

RELATIONSHIPS_KEY = "relationships"
SUPPLYER_LINE_KEY = "supplierLine"
DESTINATION_LINE_KEY = "destinationLine"
SUPPLY_ITEM_KEY = "supplyItem"
SUPPLY_NUM_KEY = "supplyNum"



class OverallLineEssence:

    ### 変数 ###
    value = dict([])


    ### 関数 ###

    def __init__(self,overallLineEssenceName:str):
        self._ReadOverallLineEssence(overallLineEssenceName)
        return
    
    def GetValue(self,key:str):
        return self.value[key]
    
    # 全体ライン本質ファイルを読み込み
    def _ReadOverallLineEssence(self,overallLineEssenceName):
        self.value = json.load(open(overallLineEssenceName,'r', encoding="utf-8"))
        return