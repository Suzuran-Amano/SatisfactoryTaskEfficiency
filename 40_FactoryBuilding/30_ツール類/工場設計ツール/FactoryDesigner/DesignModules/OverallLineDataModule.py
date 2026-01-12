import os
import json

from . import pathDataModule
from . import InfomationReaderModule as InfoReader
from . import RecipeItemModule
from . import BuildingDataManagerModule as BuildingDataModule
from . import ResourceDataModule
from . import OverallLineEssenceModule as OLineEssence


### 定数 ###
FACTORY_NAME_KEY = "factoryName"

# 一時産品関係
PRODUCTION_LIST = "productionList"
RESOURCE_NAME = "resourceName"
RESOURCE_BASE_OUTPUT_NUM = "resourceBaseOutputNum"
RESOURCE_RATIO = "resourceRatio"
BUILDING_NAME = "buildingName"
BUILDING_RATIO = "buildingRatio"
OVERCLOCK_RATIO = "overclockRatio"
TOTAL_RESOURCE_OUTPUT_NUM = "totalResourceOutputNum"

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

# 物品関係
INPUT_LINE_LIST = "inputlLineList"
OUTPUT_LINE_LIST = "outputLineList"

# フローチャート関係
RELATIONSHIPS_KEY = "relationships"
SUPPLYER_LINE_KEY = "supplierLine"
DESTINATION_LINE_KEY = "destinationLine"
SUPPLY_ITEM_KEY = "supplyItem"
SUPPLY_NUM_KEY = "supplyNum"


# 全体製造ラインデータを管理するクラス
class OverallLineData:

    ### 定数 ###
    FILE_NAME = "OverallLineData.json"


    ### 変数 ###
    _value = {}


    ### 関数 ###

    def __init__(self,data):
        # 受け入れたデータの形式により個別ラインデータの作成方法を変える
        if type(data) is OLineEssence.OverallLineEssence:
            self._value = self._MakeOLineData(data)
        elif type(data) is dict:
            self._value = data
    

    def Append(self,key,val):
        self._value[key] = val
        return
    

    # 値を取得
    def GetValue(self,key:str):
        if key in self._value:
            return self._value[key]
        return None
    
    
    # 値を取得
    def GetValueDict(self):
        return self._value
    

    def GetKeys(self):
        return self._value.keys()
    
    
    # ファイルを出力
    def Output(self,path:str):

        # パス計算
        outputPath = path + pathDataModule.OVERALL_LINE_DIRECTORY_NAME
        
        # ファイル名作成
        fileName = self.FILE_NAME

        # 書き込み
        os.makedirs(outputPath, exist_ok=True)
        jsonfile = open(outputPath + "\\" + fileName , 'w',encoding='utf-8')
        json.dump(self._value, jsonfile, indent=4,ensure_ascii=False)

        return
    
        
    # 全体ラインデータファイルの作成
    def _MakeOLineData(self,oLineEssence :OLineEssence.OverallLineEssence):

        # 返す用データを作成
        result = {}

        # 工場名
        result[FACTORY_NAME_KEY] = oLineEssence.GetValue(OLineEssence.FACTORY_NAME_KEY)

        # 資源リスト
        result = self._AppendResourceDataList(result,oLineEssence)

        # 使用レシピ
        result = self._AppendRecipeDataList(result,oLineEssence)

        # 個別ラインリスト
        result = self._AppendIndividualLineDataList(result,oLineEssence)


        # その他
        result[INPUT_LINE_LIST] = oLineEssence.GetValue(OLineEssence.INPUT_LINE_LIST)       # 入力ライン
        result[OUTPUT_LINE_LIST] = oLineEssence.GetValue(OLineEssence.OUTPUT_LINE_LIST)     # 出力ライン
        result[RELATIONSHIPS_KEY] = oLineEssence.GetValue(OLineEssence.RELATIONSHIPS_KEY)   # 製造ライン関係性

        return result
    

    # 資源データリストを追加
    def _AppendResourceDataList(
            self,
            oLine : list,
            oLineEssence :OLineEssence.OverallLineEssence
            ):
        
        # 資源辞書を準備
        list = []

        productionList = oLineEssence.GetValue(OLineEssence.PRODUCTION_LIST)
        if productionList == None:
            return oLine

        for productionData in productionList:
            list.append(self._AppendResourceData(productionData))

        oLine[PRODUCTION_LIST] = list
        
        return oLine


    # 資源データ単品を追加
    def _AppendResourceData(
            self,
            resourceDict : dict
            ):
        
        # 資源辞書を準備
        lines = {}

        # 資源名
        resourceName = resourceDict[OLineEssence.RESOURCE_NAME]
        lines[RESOURCE_NAME] = resourceName

        # 資源基本産出量
        resourceData = InfoReader.GetResourceData(resourceName)
        resourceBaseOutputNum = resourceData.GetValue(ResourceDataModule.ITEM_NUM_KEY)
        lines[RESOURCE_BASE_OUTPUT_NUM] = resourceBaseOutputNum

        # 資源倍率
        resourceRatio = resourceDict[OLineEssence.RESOURCE_RATIO]
        lines[RESOURCE_RATIO] = resourceRatio
        
        # 設備名
        buildingName = resourceDict[OLineEssence.BUILDING_NAME]
        lines[BUILDING_NAME] = buildingName

        # 設備倍率
        buildingData = InfoReader.GetBuildingData(buildingName)
        buildingRatio = buildingData.jsonData[BuildingDataModule.PRODUCTION_RATIO]
        lines[BUILDING_RATIO] = buildingRatio

        # オーバークロック倍率
        overclockRatio = resourceDict[OLineEssence.OVERCLOCK_RATIO]
        lines[OVERCLOCK_RATIO] = overclockRatio

        # 合計産出量
        lines[TOTAL_RESOURCE_OUTPUT_NUM] = resourceBaseOutputNum * resourceRatio * buildingRatio * overclockRatio


        return lines
    

    # レシピデータリストを追加
    def _AppendRecipeDataList(
            self,
            oLine : list,
            oLineEssence :OLineEssence.OverallLineEssence
            ):
        
        # レシピリストを取得
        recipeList = oLineEssence.GetValue(OLineEssence.RECIPE_LIST_KEY)
        if recipeList == None:
            return  oLine

        recipeList = []
        for useRecipe in recipeList:

            recipeItem = InfoReader.GetRecipe(useRecipe[OLineEssence.RECIPE_NAME_KEY])
            
            # レシピ情報を追加
            recipeDict = {}
            recipeDict[RECIPE_NAME_KEY] = recipeItem.GetValue(RecipeItemModule.RECIPE_NAME_KEY)   # レシピ名
            recipeDict[INPUT_LIST_KEY] = self._GetItemList(recipeItem.GetValue(RecipeItemModule.INPUT_KEY)) # 要求物品
            recipeDict[OUTPUT_LIST_KEY] = self._GetItemList(recipeItem.GetValue(RecipeItemModule.OUTPUT_KEY)) # 加工物品

            recipeList.append(recipeDict)

        oLine[RECIPE_LIST_KEY] = recipeList

        return oLine


    # レシピデータリストを追加
    def _AppendIndividualLineDataList(
            self,
            oLine : list,
            oLineEssence :OLineEssence.OverallLineEssence
            ):
        
        # レシピリストを取得
        recipeList = oLineEssence.GetValue(OLineEssence.RECIPE_LIST_KEY)
        if recipeList == None:
            return  oLine
        
        iLineList = []
        for useRecipe in recipeList:

            recipeItem = InfoReader.GetRecipe(useRecipe[OLineEssence.RECIPE_NAME_KEY])

            # レシピ情報を追加
            iLineDict = {}            
            iLineDict[INDIVIDUAL_LINE_NAME] = recipeItem.GetValue(RecipeItemModule.RECIPE_NAME_KEY) + "製造ライン"    # 製造ライン名
            iLineDict[RECIPE_NAME_KEY] = recipeItem.GetValue(RecipeItemModule.RECIPE_NAME_KEY)    # レシピ名
            recipeNum = useRecipe[OLineEssence.RECIPE_NUM_KEY]  # レシピ数
            iLineDict[RECIPE_NUM_KEY] = recipeNum
            iLineDict[INPUT_LIST_KEY] = self._GetItemList(recipeItem.GetValue(RecipeItemModule.INPUT_KEY),recipeNum)  # 要求物品
            iLineDict[OUTPUT_LIST_KEY] = self._GetItemList(recipeItem.GetValue(RecipeItemModule.OUTPUT_KEY),recipeNum)    # 加工物品

            iLineList.append(iLineDict)

        oLine[INDIVIDUAL_LINE_LIST] = iLineList

        return oLine


    # レシピ情報から、入出力の物品情報を返す
    def _GetItemList(self,itemList : list,recipeNum = 1):
        result = []
        for recipeItemData in itemList:
            itemData = {}
            itemData[ITEM_NAME_KEY] = recipeItemData[RecipeItemModule.ITEM_NAME_KEY]
            itemData[ITEM_NUM_KEY] = recipeItemData[RecipeItemModule.ITEM_NUM_KEY] * recipeNum
            result.append(itemData)

        return result
    

# 全体ラインデータファイルを読み込み
def ReadOverallLineData(oLineDataName) -> OverallLineData:
    jsonData = json.load(open(oLineDataName,'r', encoding="utf-8"))
    oLine = OverallLineData(jsonData)
    return oLine
