import os
import json

from . import pathDataModule
from .pathDataModule import PathData

class IndividualLineEssence:
    # 定数
    FILE_NAME = "IndividualLineEssence_var_lineName.json"
    LINE_NAME_REPLACE_TEXT = "var_lineName"

    LINE_NAME_KEY = "lineName"
    RECIPE_NAME_KEY = "recipeName"
    RECIPE_NUM_KEY = "recipeNum"
    SUPPLY_POWER_KEY = "supplyPower"


    # 変数
    value = []

    def __init__(self,jsonData):
        self.value = jsonData
        return
    
    # 個別製造ラインの名前を返す
    def GetLineName(self):
        return self.value[self.LINE_NAME_KEY]
    
    # レシピ名を返す
    def GetRecipeName(self):
        return self.value[self.RECIPE_NAME_KEY]
    
    # レシピ数を返す
    def GetRecipeNum(self):
        return self.value[self.RECIPE_NUM_KEY]
    
    # 供給電力を返す
    def GetSupplyPower(self):
        return self.value[self.SUPPLY_POWER_KEY]
    
    # ファイルを出力
    def Output(self,path:str):
        # パス計算
        outputPath = path + pathDataModule.INDIVIDUAL_LINE_DIRECTORY_NAME
        
        # ファイル名作成
        fileName = self.FILE_NAME.replace(self.LINE_NAME_REPLACE_TEXT,self.GetLineName())

        # 書き込み
        os.makedirs(outputPath, exist_ok=True)
        jsonfile = open(outputPath + "\\" + fileName , 'w',encoding='utf-8')
        json.dump(self.value, jsonfile, indent=4,ensure_ascii=False)

        return