import os
import json

from . import pathDataModule
from .BasicData import BasicDataReader
from .BasicData import RecipeData
from .BasicData import BuildingData
from .BasicData import BlueprintData
from .BasicData import ResourceData
from . import OverallLineEssenceModule as OLineEssence


### 定数 ###
FACTORY_NAME_KEY = "factoryName"

# 合計幅
TOTAL_WIDTH_KEY = "totalWidth"

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
BLUEPRINT_NAME = "blueprintName"
BLUEPRINT_NUM = "blueprintNum"
COLUMN_NUM = "columnNum"
INPUT_LIST_KEY = "inputList"
OUTPUT_LIST_KEY = "outputList"
ITEM_NAME_KEY = "itemName"
ITEM_NUM_KEY = "itemNum"

# 個別ライン関係
INDIVIDUAL_LINE_LIST = "individualLineList"
INDIVIDUAL_LINE_NAME = "individualLineName"
RECIPE_NUM_KEY = "recipeNum"
WIDTH_KEY = "width"

# 駅数
STATION_NUM = "stationNum"

# 物品関係
INPUT_LINE_LIST = "inputlLineList"
OUTPUT_LINE_LIST = "outputLineList"

# フローチャート関係
RELATIONSHIPS_KEY = "relationships"
SUPPLYER_LINE_KEY = "supplierLine"
DESTINATION_LINE_KEY = "destinationLine"
SUPPLY_ITEM_KEY = "supplyItem"
SUPPLY_NUM_KEY = "supplyNum"

# キーでない定数
LOAD_WIDTH = 2


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

        # 駅数計算
        station_count = 0
        input_lines = result[INPUT_LINE_LIST] or []
        output_lines = result[OUTPUT_LINE_LIST] or []
        for line in input_lines + output_lines:
            if "鉄道駅" in str(line):
                station_count += 1
        result[STATION_NUM] = station_count

        # 全体ライン幅
        existing_width = sum((line.get(WIDTH_KEY, 0) + LOAD_WIDTH) * line.get(COLUMN_NUM, 1) for line in result.get(INDIVIDUAL_LINE_LIST, [])) + LOAD_WIDTH
        station_based_width = station_count * 7 + 7
        result[TOTAL_WIDTH_KEY] = max(existing_width, station_based_width)
        print("製造ライン幅 : " + str(existing_width))
        print("駅幅 : " + str(station_based_width))

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
        resourceData = BasicDataReader.GetResourceData(resourceName)
        resourceBaseOutputNum = resourceData.GetValue(ResourceData.ITEM_NUM_KEY)
        lines[RESOURCE_BASE_OUTPUT_NUM] = resourceBaseOutputNum

        # 資源倍率
        resourceRatio = resourceDict[OLineEssence.RESOURCE_RATIO]
        lines[RESOURCE_RATIO] = resourceRatio
        
        # 設備名
        buildingName = resourceDict[OLineEssence.BUILDING_NAME]
        lines[BUILDING_NAME] = buildingName

        # 設備倍率
        buildingData = BasicDataReader.GetBuildingData(buildingName)
        buildingRatio = buildingData.jsonData[BuildingData.PRODUCTION_RATIO]
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

        recipeLine = []
        for useRecipe in recipeList:
            recipeData = BasicDataReader.GetRecipe(useRecipe[OLineEssence.RECIPE_NAME_KEY])
            
            # レシピ情報を追加
            recipeDict = {}
            recipeDict[RECIPE_NAME_KEY] = recipeData.GetValue(RecipeData.RECIPE_NAME_KEY)   # レシピ名
            recipeDict[INPUT_LIST_KEY] = self._GetItemList(recipeData.GetValue(RecipeData.INPUT_KEY)) # 要求物品
            recipeDict[OUTPUT_LIST_KEY] = self._GetItemList(recipeData.GetValue(RecipeData.OUTPUT_KEY)) # 加工物品

            recipeLine.append(recipeDict)

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

        iLineList = [self._AppendIndividualLineDataItem(useRecipe) for useRecipe in recipeList]

        oLine[INDIVIDUAL_LINE_LIST] = iLineList

        return oLine


    # 個別ラインのデータを1つ作成
    def _AppendIndividualLineDataItem(self, useRecipe):
        recipeData = BasicDataReader.GetRecipe(useRecipe[OLineEssence.RECIPE_NAME_KEY])

        # レシピ情報を追加
        iLineDict = {}
        # 製造ライン名
        iLineDict[INDIVIDUAL_LINE_NAME] = recipeData.GetValue(RecipeData.RECIPE_NAME_KEY) + "製造ライン"

        # レシピ名
        iLineDict[RECIPE_NAME_KEY] = recipeData.GetValue(RecipeData.RECIPE_NAME_KEY)

        # レシピ数など
        recipeNum = 0
        if OLineEssence.RECIPE_NUM_KEY in useRecipe:  # レシピ数で指定されている場合
            # レシピ数
            recipeNum = useRecipe[OLineEssence.RECIPE_NUM_KEY]  
            iLineDict[RECIPE_NUM_KEY] = recipeNum

        else: # 青写真で指定されている場合
            # 青写真名
            blueprintName = useRecipe[OLineEssence.BLUEPRINT_NAME]  
            iLineDict[BLUEPRINT_NAME] = blueprintName

            # 青写真数
            blueprintNum = useRecipe[OLineEssence.BLUEPRINT_NUM]  
            iLineDict[BLUEPRINT_NUM] = blueprintNum

            # レシピ数
            blueprintData = BasicDataReader.GetBlueprintData(blueprintName)
            count = blueprintData.GetValue(BlueprintData.COUNT)
            recipeNum = count * blueprintNum
            iLineDict[RECIPE_NUM_KEY] = recipeNum
            
            # 青写真幅
            iLineDict[WIDTH_KEY] = blueprintData.GetValue(BlueprintData.WIDTH)

        # 列数
        columnNum = 1
        if OLineEssence.COLUMN_NUM in useRecipe:
            columnNum = useRecipe[OLineEssence.COLUMN_NUM]
        iLineDict[COLUMN_NUM] = columnNum

        # 要求物品
        iLineDict[INPUT_LIST_KEY] = self._GetItemList(recipeData.GetValue(RecipeData.INPUT_KEY), recipeNum)
        # 加工物品 
        iLineDict[OUTPUT_LIST_KEY] = self._GetItemList(recipeData.GetValue(RecipeData.OUTPUT_KEY), recipeNum)

        return iLineDict
    

    # レシピ情報から、入出力の物品情報を返す
    def _GetItemList(self,itemList : list,recipeNum = 1):
        result = []
        for recipeDataData in itemList:
            itemData = {}
            itemData[ITEM_NAME_KEY] = recipeDataData[RecipeData.ITEM_NAME_KEY]
            itemData[ITEM_NUM_KEY] = recipeDataData[RecipeData.ITEM_NUM_KEY] * recipeNum
            result.append(itemData)

        return result



# 全体ラインデータファイルを読み込み
def ReadOverallLineData(oLineDataName) -> OverallLineData:
    jsonData = json.load(open(oLineDataName,'r', encoding="utf-8"))
    oLine = OverallLineData(jsonData)
    return oLine
