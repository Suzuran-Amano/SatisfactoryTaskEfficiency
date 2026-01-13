import os
import json

from . import pathDataModule
from . import InfomationReaderModule as InfoReader
from . import RecipeItemModule
from . import ResourceDataModule
from . import BuildingDataManagerModule as BuildingData
from . import ResourceLineEssenceModule as RLineEssence


### 定数 ###
LINE_NAME_KEY = "lineName"

# 一時産品関係
LINE_NAME_KEY = "lineName"
RESOURCE_NAME_KEY = "resourceName"
RESOURCE_BASE_OUTPUT_NUM = "resourceBaseOutputNum"

RESOURCE_LIST_KEY = "resourceList"
RESOURCE_RATIO_KEY = "resourceRatio"
BUILDING_NAME_KEY = "buildingName"
OVERCLOCK_RATIO_KEY = "overclockRatio"
SINGLE_RESOURCE_OUTPUT_NUM = "singleResourceOutputNum"
TOTAL_RESOURCE_OUTPUT_NUM = "totalResourceOutputNum"
USE_POWER_KEY = "usePower"
TOTAL_USE_POWER_KEY = "totalUsePower"

# 設備関係
PRODUCT_NAME_KEY = "productName"
TOTAL_USE_POWER_KEY = "totalUsePower"

# コスト関係
COST_LIST_KEY = "costList"
ITEM_NAME_KEY = "itemName"
ITEM_NUM_KEY = "itemNum"


# 個別製造ラインデータを管理するクラス
class ResourceLineData:

    ### 定数 ###
    FILE_NAME = "ResourceLineData_var_lineName.json"
    LINE_NAME_REPLACE_TEXT = "var_lineName"


    ### 変数 ###
    _value = {}


    ### 関数 ###

    def __init__(self,data):
        # 受け入れたデータの形式により資源産出ラインデータの作成方法を変える
        if type(data) is RLineEssence.ResourceLineEssence:
            self._value = self._RLineDataToEssence(data)
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
        outputPath = path + pathDataModule.INDIVIDUAL_LINE_DIRECTORY_NAME
        
        # ファイル名作成
        fileName = self.FILE_NAME.replace(self.LINE_NAME_REPLACE_TEXT,self.GetValue(LINE_NAME_KEY))

        # 書き込み
        os.makedirs(outputPath, exist_ok=True)
        jsonfile = open(outputPath + "\\" + fileName , 'w',encoding='utf-8')
        json.dump(self._value, jsonfile, indent=4,ensure_ascii=False)

        return
    


    # 資源産出ライン本質から資源産出ラインデータを作成
    def _RLineDataToEssence(
            self,
            rLineEssence : RLineEssence.ResourceLineEssence
            ) -> dict:
        
        # 必要な情報を取得
        resourceData = InfoReader.GetResourceData(rLineEssence.GetValue(RLineEssence.RESOURCE_NAME_KEY))
        buildingList = {}
        resourceList = rLineEssence.GetValue(RLineEssence.RESOURCE_LIST_KEY)
        for resourceItem in resourceList:
            if not(resourceItem[BUILDING_NAME_KEY] in buildingList):
                buildingList[resourceItem[BUILDING_NAME_KEY]] = InfoReader.GetBuildingData(resourceItem[BUILDING_NAME_KEY])

        # 返す用のデータ
        rLineData = {}

        # ライン名を追加
        rLineData[LINE_NAME_KEY] = rLineEssence.GetValue(RLineEssence.LINE_NAME_KEY)

        # 資源情報
        rLineData[RESOURCE_NAME_KEY] = resourceData.GetValue(ResourceDataModule.RESOURCE_NAME_KEY)
        resourceBaseOutputNum = resourceData.GetValue(ResourceDataModule.ITEM_NUM_KEY)
        rLineData[RESOURCE_BASE_OUTPUT_NUM] = resourceBaseOutputNum

        # 資源リスト
        rLineData[RESOURCE_LIST_KEY] = resourceList

        # 各資源の情報
        rLineData[TOTAL_RESOURCE_OUTPUT_NUM] = 0
        rLineData[TOTAL_USE_POWER_KEY] = 0
        for resourceItem in resourceList:
            resourceRatio = resourceItem[RESOURCE_RATIO_KEY]
            overclockRatio = resourceItem[OVERCLOCK_RATIO_KEY]
            buildingData = buildingList[resourceItem[BUILDING_NAME_KEY]]
            buildingUsePower = buildingData.GetValue(BuildingData.USE_POWER_KEY)
            buildingRatio = buildingData.GetValue(BuildingData.PRODUCTION_RATIO)
            
            # 産出量を計算
            singleOutput = resourceBaseOutputNum * resourceRatio * buildingRatio * overclockRatio
            resourceItem[SINGLE_RESOURCE_OUTPUT_NUM] = singleOutput
            rLineData[TOTAL_RESOURCE_OUTPUT_NUM] += singleOutput

            # 消費電力            
            usePower = buildingUsePower * overclockRatio ** 1.321928
            resourceItem[USE_POWER_KEY] = usePower
            rLineData[TOTAL_USE_POWER_KEY] += usePower

                  
        return rLineData
    
    
# 資源産出ラインデータファイルを読み込み
def ReadResourceLineData(iLineDataName) -> ResourceLineData:
    jsonData = json.load(open(iLineDataName,'r', encoding="utf-8"))
    oLineData = ResourceLineData(jsonData)
    return oLineData