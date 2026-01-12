import os
import json

from . import pathDataModule
from . import OverallLineDataModule as OLineDataModule


# 定数
LINE_NAME_KEY = "lineName"
RESOURCE_NAME_KEY = "resourceName"

RESOURCE_LIST_KEY = "resourceList"
RESOURCE_RATIO_KEY = "resourceRatio"
BUILDING_RATIO_KEY = "buildingName"
OVERCLOCK_RATIO = "overclockRatio"


# 資源産出ライン本質ファイルを読み込み
def ReadResourceLineFile(inputDataFileName):
    jsonData = json.load(open(inputDataFileName,'r', encoding="utf-8"))
    ResourceLine = ResourceLineEssence(jsonData)
    return ResourceLine


# 資源産出ライン本質の管理クラス
class ResourceLineEssence:
    # 定数
    FILE_NAME = "ResourceLineEssence_var_lineName.json"
    LINE_NAME_REPLACE_TEXT = "var_lineName"


    # 変数
    _value = {}

    def __init__(self,data,resourceName=None):
        # 受け入れたデータの形式により個別ラインデータの作成方法を変える
        if type(data) is OLineDataModule.OverallLineData:
            self._value = self._MakeRLineEssenceToOLineData(data,resourceName)
        elif type(data) is dict:
            self._value = data
        return
    

    def _MakeRLineEssenceToOLineData(
            self,
            oLineData : OLineDataModule.OverallLineData,
            resourceName : str
            ) -> dict:
        
        resourceList = oLineData.GetValue(OLineDataModule.PRODUCTION_LIST)

        result = {}

        result[LINE_NAME_KEY] = resourceName + "産出ライン"
        result[RESOURCE_NAME_KEY] = resourceName

        
        resourceLine = []
        for resourceItem in resourceList:
            resourceDict = {}
            resourceDict[RESOURCE_RATIO_KEY] = resourceItem[OLineDataModule.RESOURCE_RATIO]
            resourceDict[BUILDING_RATIO_KEY] = resourceItem[OLineDataModule.BUILDING_RATIO]
            resourceDict[OVERCLOCK_RATIO]    = resourceItem[OLineDataModule.OVERCLOCK_RATIO]
            resourceLine.append(resourceDict)

        result[RESOURCE_LIST_KEY] = resourceLine


        return result
    
    
    # 値を返す
    def GetValue(self,key:str):
        if key in self._value:
            return self._value[key]
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
        json.dump(self._value, jsonfile, indent=4,ensure_ascii=False)

        return