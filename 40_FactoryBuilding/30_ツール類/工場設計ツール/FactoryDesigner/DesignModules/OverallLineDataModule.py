import os
import json

from . import pathDataModule
from . import OverallLineEssenceModule as OLineEssence
from . import InfomationReaderModule as RecipeReader
from . import RecipeItemModule as RecipeItem


### 定数 ###
FILE_NAME = "OverallLineData.json"

REPLACE_KEY_HEADER = "var_"

FACTORY_NAME_KEY = "factoryName"

# 一時産品関係
PRODUCTION_LIST = "productionList"
BUILDING_NAME = "buildingName"
RESOURCE_RATIO = "resourceRatio"
OVERCLOCK_RATIO = "overclockRatio"

# レシピ関係
RECIPE_LIST_KEY = "recipeList"
RECIPE_NAME_KEY = "recipeName"
INPUT_LIST_KEY = "inputList"
OUTPUT_LIST_KEY = "outputList"
ITEM_NAME_KEY = "itemName"
ITEM_NUM_KEY = "itemNum"

# 個別ライン関係
INDIVIDUAL_LINE_LIST = "individualLineList"
INDIVIDUAL_LINE_NAME = "individualLineName"
RECIPE_NUM_KEY = "recipeNum"

# 材料関係
INPUT_LINE_LIST = "inputlLineList"
OUTPUT_LINE_LIST = "outputLineList"

# フローチャート関係
RELATIONSHIPS_KEY = "relationships"
SUPPLYER_LINE_KEY = "supplierLine"
DESTINATION_LINE_KEY = "destinationLine"
SUPPLY_ITEM_KEY = "supplyItem"
SUPPLY_NUM_KEY = "supplyNum"


class OverallLineData:


    ### 変数 ###
    value = {}


    ### 関数 ###

    def __init__(self,oLineEssence :OLineEssence.OverallLineEssence):
        self.value = self._MakeOLineData(oLineEssence)
        return
    
    # 値を返す
    def GetValue(self,key:str):
        return self.value[key]
    
    # ファイルを出力
    def Output(self,path:str):

        outputPath = path + pathDataModule.OVERALL_LINE_DIRECTORY_NAME
        
        # 書き込み
        os.makedirs(outputPath, exist_ok=True)
        jsonfile = open(outputPath + "\\" + FILE_NAME , 'w',encoding='utf-8')
        json.dump(self.value, jsonfile, indent=4,ensure_ascii=False)

        return
    

        
    # 全体ラインデータファイルの作成
    def _MakeOLineData(self,oLineEssence :OLineEssence.OverallLineEssence):

        # 返す用データを作成
        result = {}

        # 工場名
        result[FACTORY_NAME_KEY] = oLineEssence.GetValue(OLineEssence.FACTORY_NAME_KEY)

        # 一時産品リスト
        result[PRODUCTION_LIST] = oLineEssence.GetValue(OLineEssence.PRODUCTION_LIST)

        # 使用レシピ
        recipeList = []
        for useRecipe in oLineEssence.GetValue(OLineEssence.RECIPE_LIST_KEY):

            recipeItem = RecipeReader.GetRecipe(useRecipe[OLineEssence.RECIPE_NAME_KEY])
            
            # レシピ情報を追加
            recipeDict = {}
            recipeDict[RECIPE_NAME_KEY] = recipeItem.GetValue(RecipeItem.RECIPE_NAME_KEY)   # レシピ名
            recipeDict[INPUT_LIST_KEY] = self._GetItemList(recipeItem.GetValue(RecipeItem.INPUT_KEY)) # 要求物品
            recipeDict[OUTPUT_LIST_KEY] = self._GetItemList(recipeItem.GetValue(RecipeItem.OUTPUT_KEY)) # 加工物品

            recipeList.append(recipeDict)

        result[RECIPE_LIST_KEY] = recipeList


        # 個別ラインリスト
        iLineList = []
        for useRecipe in oLineEssence.GetValue(OLineEssence.RECIPE_LIST_KEY):

            recipeItem = RecipeReader.GetRecipe(useRecipe[OLineEssence.RECIPE_NAME_KEY])

            # レシピ情報を追加
            iLineDict = {}            
            iLineDict[INDIVIDUAL_LINE_NAME] = recipeItem.GetValue(RecipeItem.RECIPE_NAME_KEY) + "製造ライン"    # 製造ライン名
            iLineDict[RECIPE_NAME_KEY] = recipeItem.GetValue(RecipeItem.RECIPE_NAME_KEY)    # レシピ名
            recipeNum = useRecipe[OLineEssence.RECIPE_NUM_KEY]  # レシピ数
            iLineDict[RECIPE_NUM_KEY] = recipeNum
            iLineDict[INPUT_LIST_KEY] = self._GetItemList(recipeItem.GetValue(RecipeItem.INPUT_KEY),recipeNum)  # 要求物品
            iLineDict[OUTPUT_LIST_KEY] = self._GetItemList(recipeItem.GetValue(RecipeItem.OUTPUT_KEY),recipeNum)    # 加工物品

            iLineList.append(iLineDict)

        result[INDIVIDUAL_LINE_LIST] = iLineList


        # その他
        result[INPUT_LINE_LIST] = oLineEssence.GetValue(OLineEssence.INPUT_LINE_LIST)       # 入力ライン
        result[OUTPUT_LINE_LIST] = oLineEssence.GetValue(OLineEssence.OUTPUT_LINE_LIST)     # 出力ライン
        result[RELATIONSHIPS_KEY] = oLineEssence.GetValue(OLineEssence.RELATIONSHIPS_KEY)   # 製造ライン関係性

        return result
    

    # レシピ情報から、入出力の物品情報を返す
    def _GetItemList(self,itemList : list,recipeNum = 1):
        result = []
        for recipeItemData in itemList:
            itemData = {}
            itemData[ITEM_NAME_KEY] = recipeItemData[RecipeItem.ITEM_NAME_KEY]
            itemData[ITEM_NUM_KEY] = recipeItemData[RecipeItem.ITEM_NUM_KEY] * recipeNum
            result.append(itemData)

        return result


# 全体ラインデータファイルを読み込み
def ReadOverallLineData(overallLineDataName) -> OverallLineData:
    jsonData = json.load(open(overallLineDataName,'r', encoding="utf-8"))
    overallLine = OverallLineData(jsonData)
    return overallLine
