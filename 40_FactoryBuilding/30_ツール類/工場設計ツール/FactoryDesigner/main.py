import sys
import json

from DesignModules import pathDataModule
import MakeOverallLineDesign
import MakeIndividualLineDesign
import MakeIndividualLineCheckList


# パス情報を作成
pathData = pathDataModule.PathData(sys.argv)

# 全体製造ライン設計書作成
oDesignMaker = MakeOverallLineDesign.OverallLineDesignMaker()
oLineData = oDesignMaker.Main(pathData)


# 個別製造ライン設計書作成
iLineEssences = oDesignMaker.individualLineEssences
iLineDataList = []
usePow = 0
for iLineEssence in iLineEssences:
    iDesignMaker = MakeIndividualLineDesign.IndividualLineDesignMaker()
    iLineData = iDesignMaker.Main(pathData,iLineEssence)
    usePow += iLineData.GetTotalUsePower()
    iLineDataList.append(iLineData)


# 個別製造ラインテスト項目書作成
for iLineEssence in iLineEssences:
    checkListMaker = MakeIndividualLineCheckList.MakeIndividualLineCheckList()
    checkListMaker.Main(pathData,iLineEssence)


# 工場データ出力
factoryData = {}
factoryData["factoryName"] = oLineData.GetValue(oLineData.FACTORY_NAME_KEY) # 工場名
factoryData["usePower"] = usePow    # 消費電力

jsonfile = open(pathData.GetPath() + '/' + "FactoryData" + '.json', 'w',encoding='utf-8')
json.dump(factoryData, jsonfile, indent=4,ensure_ascii=False)