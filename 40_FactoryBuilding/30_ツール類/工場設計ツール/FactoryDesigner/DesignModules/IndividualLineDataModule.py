import os
import json

from . import pathDataModule
from DesignModules import InfomationReaderModule as InfoReader
from DesignModules import RecipeItemModule as RecipeItem
from DesignModules import BuildingDataManagerModule as BuildingData
from DesignModules import IndividualLineEssenceModule as ILineEssence


# 定数
REPLACE_KEY_HEADER = "var_"
LINE_NAME_KEY = "lineName"
RECIPE_NAME_KEY = "recipeName"
RECIPE_NUM_KEY = "recipeNum"
PRODUCT_NAME_KEY = "productName"
TOTAL_USE_POWER_KEY = "totalUsePower"
INPUT_NAME_KEY = "inputName"
INPUT_NUM_KEY = "inputNum"
OUTPUT_NAME_KEY = "outputName"
OUTPUT_NUM_KEY = "outputNum"
TOTAL_INPUT_KEY = "totalInput"
TOTAL_OUTPUT_KEY = "totalOutput"

COST_LIST_KEY = "costList"
ITEM_NAME_KEY = "itemName"
ITEM_NUM_KEY = "itemNum"
SUPPLY_POWER_KEY = "supplyPower"


class IndividualLineData:
    # 定数
    FILE_NAME = "IndividualLineData_var_lineName.json"
    LINE_NAME_REPLACE_TEXT = "var_lineName"


    ### 変数 ###
    _value = dict


    ### 関数 ###

    def __init__(self,data):
        if type(data) is ILineEssence.IndividualLineEssence:
            self._value = self._ILineEssenceToData(data)
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
    
    
    def GetKeys(self):
        return self._value.keys()
    
    def GetReplaceKey(self,key):
        return REPLACE_KEY_HEADER + key
    
    # ファイルを出力
    def Output(self,path:str):
        
        # パス計算
        outputPath = path + pathDataModule.INDIVIDUAL_LINE_DIRECTORY_NAME
        
        # ファイル名作成
        fileName = self.FILE_NAME.replace(self.LINE_NAME_REPLACE_TEXT,self.GetValue(LINE_NAME_KEY))

        # 書き込み
        os.makedirs(outputPath, exist_ok=True)
        jsonfile = open(outputPath + "\\" + fileName , 'w',encoding='utf-8')
        json.dump(self._value, jsonfile, indent=4,ensure_ascii=False)

        return
    


    # 個別ライン本質から個別ラインデータを作成
    def _ILineEssenceToData(
            self,
            iLineEssence : ILineEssence.IndividualLineEssence
            ) -> dict:
        
        # 返す用のデータ
        iLineData = {}

        # 基礎情報を取得
        recipeItem = InfoReader.GetRecipe(iLineEssence.GetValue(ILineEssence.RECIPE_NAME_KEY))
        buildingData = InfoReader.GetBuildingData(recipeItem.GetValue(RecipeItem.PRODUCT_NAME_KEY))


        # ライン名を追加
        iLineData[LINE_NAME_KEY] = iLineEssence.GetValue(ILineEssence.LINE_NAME_KEY)

        # レシピ名を追加
        iLineData[RECIPE_NAME_KEY] = recipeItem.GetValue(RecipeItem.RECIPE_NAME_KEY)
        recipeNum = iLineEssence.GetValue(ILineEssence.RECIPE_NUM_KEY)
        iLineData[RECIPE_NUM_KEY] = recipeNum

        # 制作物を追加
        productName = recipeItem.GetValue(RecipeItem.PRODUCT_NAME_KEY)
        iLineData[PRODUCT_NAME_KEY] = productName

        # 合計コストを追加
        buildingData = InfoReader.GetBuildingData(productName)
        costList = []
        for cost in buildingData.GetValue(BuildingData.COST_KEY):
            costList.append({
                ITEM_NAME_KEY : cost[BuildingData.ITEM_NAME_KEY],
                ITEM_NUM_KEY : cost[BuildingData.ITEM_NUM_KEY] * recipeNum

            })
        iLineData[COST_LIST_KEY] = costList


        # 合計消費電力を追加
        totalUsePower = buildingData.GetValue(BuildingData.USE_POWER_KEY) * recipeNum
        iLineData[TOTAL_USE_POWER_KEY] = totalUsePower

        # 搬入物を追加
        index = 0
        for data in recipeItem.GetValue(RecipeItem.INPUT_KEY):
            inputNameKey = INPUT_NAME_KEY + str(index+1)
            inputName = data[RecipeItem.ITEM_NAME_KEY]
            iLineData[inputNameKey] = inputName
            
            inputNumKey = INPUT_NUM_KEY + str(index+1)
            inputNum = data[RecipeItem.ITEM_NUM_KEY]
            iLineData[inputNumKey] = inputNum
            
            inputTotalKey = TOTAL_INPUT_KEY + str(index+1)
            inputTotal = recipeNum*inputNum
            iLineData[inputTotalKey] = inputTotal
            
            index = index + 1
        
        # 搬出物を追加
        index = 0
        for data in recipeItem.GetValue(RecipeItem.OUTPUT_KEY):
            outputNameKey = OUTPUT_NAME_KEY + str(index+1)
            outputName = data[RecipeItem.ITEM_NAME_KEY]
            iLineData[outputNameKey] = outputName
            
            outputNumKey = OUTPUT_NUM_KEY + str(index+1)
            outputNum = data[RecipeItem.ITEM_NUM_KEY]
            iLineData[outputNumKey] = outputNum
            
            outputTotalKey = TOTAL_OUTPUT_KEY + str(index+1)
            outputTotal = recipeNum*outputNum
            iLineData[outputTotalKey] = outputTotal

            index = index + 1

        # 供給電力を追加
        supplyPower = recipeItem.GetValue(RecipeItem.SUPPLY_POWER_KEY)
        if supplyPower == None:
            supplyPower = 0
        supplyPower = supplyPower * recipeNum
        iLineData[SUPPLY_POWER_KEY] = supplyPower

                    
        return iLineData