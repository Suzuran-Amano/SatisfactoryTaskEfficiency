import os
import json

from . import pathDataModule
from .pathDataModule import PathData


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
    _value = dict([])


    ### 関数 ###
   
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
    