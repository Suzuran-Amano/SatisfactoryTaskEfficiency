import sys
import json

from DesignModules import pathDataModule
from DesignModules import OverallLineDataModule as OLineData
from DesignModules import ResourceLineEssenceModule as RLineEssence
from DesignModules import IndividualLineDataModule as ILineData
import MakeOverallLineDesign
import MakeIndividualLineDesign
import MakeIndividualLineCheckList


# パス情報を作成
pathData = pathDataModule.PathData(sys.argv)

# 工場データの準備
usePow = 0
costList = {}
supplyPower = 0


# 全体製造ライン設計書作成
oDesignMaker = MakeOverallLineDesign.OverallLineDesignMaker()
oLineData = oDesignMaker.Main(pathData)


# 資源産出ライン設計書作成
rLineDataList = []

resourceNameList = []
for productionItem in oLineData.GetValue(OLineData.PRODUCTION_LIST):
    resourceName = productionItem[OLineData.RESOURCE_NAME]
    if not(resourceName in resourceNameList):
        resourceNameList.append(resourceName)

for resourceName in resourceNameList:
    rLineData = RLineEssence.ResourceLineEssence(oLineData,resourceName)
    rLineData.Output(pathData.GetPath())

    


# 個別製造ライン設計書作成
iLineEssences = oDesignMaker.individualLineEssences
iLineDataList = []
for iLineEssence in iLineEssences:
    iDesignMaker = MakeIndividualLineDesign.IndividualLineDesignMaker()
    iLineData = iDesignMaker.Main(pathData,iLineEssence)
    iLineDataList.append(iLineData)

    # 工場データ計算
    usePow += iLineData.GetValue(ILineData.TOTAL_USE_POWER_KEY)
    supplyPower += iLineData.GetValue(ILineData.SUPPLY_POWER_KEY)

    itemNameKey = ILineData.ITEM_NAME_KEY
    itemNumKey = ILineData.ITEM_NUM_KEY
    for cost in iLineData.GetValue(ILineData.COST_LIST_KEY):
        if cost[itemNameKey] in costList:
            costList[cost[itemNameKey]] += cost[itemNumKey]
        else:            
            costList[cost[itemNameKey]] = cost[itemNumKey]

# 個別製造ラインテスト項目書作成
for iLineData in iLineDataList:
    checkListMaker = MakeIndividualLineCheckList.MakeIndividualLineCheckList()
    checkListMaker.Main(pathData,iLineData)


# 工場データ出力
factoryData = {}
factoryData["factoryName"] = oLineData.GetValue(OLineData.FACTORY_NAME_KEY) # 工場名
factoryData["usePower"] = usePow    # 消費電力
factoryData["costList"] = costList
factoryData["supplyPower"] = supplyPower

jsonfile = open(pathData.GetPath() + '/' + "FactoryData" + '.json', 'w',encoding='utf-8')
json.dump(factoryData, jsonfile, indent=4,ensure_ascii=False)