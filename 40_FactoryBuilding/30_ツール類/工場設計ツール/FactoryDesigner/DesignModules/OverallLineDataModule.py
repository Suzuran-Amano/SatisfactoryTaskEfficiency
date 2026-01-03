import os
import json

from . import pathDataModule
from . import OverallLineEssenceModule as OLineEssence
from . import RecipeReaderModule as RecipeReader
from . import RecipeItemModule as RecipeItem


### 定数 ###
FILE_NAME = "OverallLineData.json"

REPLACE_KEY_HEADER = "var_"

FACTORY_NAME_KEY = "factoryName"

RECIPE_LIST_KEY = "recipeList"
RECIPE_NAME_KEY = "recipeName"
INPUT_LIST_KEY = "inputList"
OUTPUT_LIST_KEY = "outputList"
ITEM_NAME_KEY = "itemName"
ITEM_NUM_KEY = "itemNum"

INDIVIDUAL_LINE_LIST = "individualLineList"
INDIVIDUAL_LINE_NAME = "individualLineName"
RECIPE_NUM_KEY = "recipeNum"

INPUT_LINE_LIST = "inputlLineList"
OUTPUT_LINE_LIST = "outputLineList"

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

        
        # 使用レシピ
        recipeList = []
        for useRecipe in oLineEssence.GetValue(OLineEssence.RECIPE_LIST_KEY):

            recipeData = RecipeReader.GetRecipe(useRecipe[OLineEssence.RECIPE_NAME_KEY])
            
            recipeDict = {}

            # レシピ名
            recipeDict[RECIPE_NAME_KEY] = recipeData.GetRecipeName()

            # 要求物品
            recipeDict[INPUT_LIST_KEY] = self.GetItemList(recipeData.GetInputItemList())

            # 加工物品
            recipeDict[OUTPUT_LIST_KEY] = self.GetItemList(recipeData.GetOutputItemList())

            recipeList.append(recipeDict)

        result[RECIPE_LIST_KEY] = recipeList


        # 個別ラインリスト
        iLineList = []
        for useRecipe in oLineEssence.GetValue(OLineEssence.RECIPE_LIST_KEY):

            recipeData = RecipeReader.GetRecipe(useRecipe[OLineEssence.RECIPE_NAME_KEY])

            iLineDict = {}

            # 製造ライン名
            iLineDict[INDIVIDUAL_LINE_NAME] = recipeData.GetRecipeName() + "製造ライン"

            # レシピ名
            iLineDict[RECIPE_NAME_KEY] = recipeData.GetRecipeName()
          
            # レシピ数
            recipeNum = useRecipe[OLineEssence.RECIPE_NUM_KEY]
            iLineDict[RECIPE_NUM_KEY] = recipeNum

            # 要求物品
            iLineDict[INPUT_LIST_KEY] = self.GetItemList(recipeData.GetInputItemList(),recipeNum)

            # 加工物品
            iLineDict[OUTPUT_LIST_KEY] = self.GetItemList(recipeData.GetOutputItemList(),recipeNum)

            iLineList.append(iLineDict)

        result[INDIVIDUAL_LINE_LIST] = iLineList


        # 入力ライン
        result[INPUT_LINE_LIST] = oLineEssence.GetValue(OLineEssence.INPUT_LINE_LIST)
        
        # 出力ライン
        result[OUTPUT_LINE_LIST] = oLineEssence.GetValue(OLineEssence.OUTPUT_LINE_LIST)
        
        # 製造ライン関係性
        result[RELATIONSHIPS_KEY] = oLineEssence.GetValue(OLineEssence.RELATIONSHIPS_KEY)

        return result
    

    # レシピ情報から、入出力の物品情報を返す
    def GetItemList(self,itemList : list,recipeNum = 1):
        result = []
        for recipeItemData in itemList:
            itemData = {}
            itemData[ITEM_NAME_KEY] = recipeItemData[RecipeItem.ITEM_NAME_KEY]
            itemData[ITEM_NUM_KEY] = recipeItemData[RecipeItem.ITEM_NUM_KEY] * recipeNum
            result.append(itemData)

        return result


