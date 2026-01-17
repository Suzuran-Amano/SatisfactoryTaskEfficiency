import os
import json

from . import pathDataModule
from .pathDataModule import PathData


# 定数
LINE_NAME_KEY = "lineName"
RECIPE_NAME_KEY = "recipeName"
BLUEPRINT_NAME = "blueprintName"
BLUEPRINT_NUM = "blueprintNum"
RECIPE_NUM_KEY = "recipeNum"
SUPPLY_POWER_KEY = "supplyPower"



# 個別ライン本質ファイルを読み込み
def ReadIndividualLineFile(inputDataFileName):
    jsonData = json.load(open(inputDataFileName,'r', encoding="utf-8"))
    individualLine = IndividualLineEssence(jsonData)
    return individualLine


# 個別ライン本質の管理クラス
class IndividualLineEssence:
    # 定数
    FILE_NAME = "IndividualLineEssence_var_lineName.json"
    LINE_NAME_REPLACE_TEXT = "var_lineName"


    # 変数
    value = {}

    def __init__(self,jsonData):
        self.value = jsonData
        return
    
    
    # 値を返す
    def GetValue(self,key:str):
        if key in self.value:
            return self.value[key]
        return None
    

    # ファイルを出力
    def Output(self,path:str):
        # パス計算
        outputPath = path + pathDataModule.INDIVIDUAL_LINE_DIRECTORY_NAME
        
        # ファイル名作成
        fileName = self.FILE_NAME.replace(self.LINE_NAME_REPLACE_TEXT,self.GetValue(LINE_NAME_KEY))

        # 書き込み
        os.makedirs(outputPath, exist_ok=True)
        jsonfile = open(outputPath + "\\" + fileName , 'w',encoding='utf-8')
        json.dump(self.value, jsonfile, indent=4,ensure_ascii=False)

        return