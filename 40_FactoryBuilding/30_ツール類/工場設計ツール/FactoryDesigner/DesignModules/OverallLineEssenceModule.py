import json

### 定数 ###
FACTORY_NAME_KEY = "factoryName"

PRODUCTION_LIST = "productionList"
RESOURCE_NAME = "resourceName"
BUILDING_NAME = "buildingName"
RESOURCE_RATIO = "resourceRatio"
OVERCLOCK_RATIO = "overclockRatio"

RECIPE_LIST_KEY = "recipeList"
RECIPE_NAME_KEY = "recipeName"
RECIPE_NUM_KEY = "recipeNum"
BLUEPRINT_NAME = "blueprintName"
BLUEPRINT_NUM = "blueprintNum"
COLUMN_NUM = "columnNum"

INPUT_LINE_LIST = "inputlLineList"
OUTPUT_LINE_LIST = "outputLineList"

RELATIONSHIPS_KEY = "relationships"
SUPPLYER_LINE_KEY = "supplierLine"
DESTINATION_LINE_KEY = "destinationLine"
SUPPLY_ITEM_KEY = "supplyItem"
SUPPLY_NUM_KEY = "supplyNum"



class OverallLineEssence:

    ### 変数 ###
    _value = dict([])


    ### 関数 ###

    def __init__(self,overallLineEssenceName:str):
        self._ReadOverallLineEssence(overallLineEssenceName)
        return
    
    
    # 全体ライン本質ファイルを読み込み
    def _ReadOverallLineEssence(self,overallLineEssenceName):
        self._value = json.load(open(overallLineEssenceName,'r', encoding="utf-8"))
        return
    
    
    # 値を返す
    def GetValue(self,key:str):
        if key in self._value:
            return self._value[key]