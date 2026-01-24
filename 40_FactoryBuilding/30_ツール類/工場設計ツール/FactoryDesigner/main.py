import sys

from DesignModules import pathDataModule
from DesignModules import FactoryDataOutputModule
from DesignModules import OverallLineDataModule as OLineData
from DesignModules import ResourceLineEssenceModule as RLineEssence
from DesignModules import ResourceLineDataModule as RLineData
from DesignModules import ResourceLineDocumentModule as RLineDoc

import MakeOverallLineDesign
import MakeIndividualLineDesign
import MakeIndividualLineCheckList


# パス情報を作成
pathData = pathDataModule.PathData(sys.argv)


# 全体製造ライン設計書作成
oDesignMaker = MakeOverallLineDesign.OverallLineDesignMaker()
oLineData = oDesignMaker.Main(pathData)


# 資源産出ライン設計書作成
rLineEssenceList = []

resourceNameList = []
productionList = oLineData.GetValue(OLineData.PRODUCTION_LIST)
if not(productionList == None):
    for productionItem in oLineData.GetValue(OLineData.PRODUCTION_LIST):
        resourceName = productionItem[OLineData.RESOURCE_NAME]
        if not(resourceName in resourceNameList):
            resourceNameList.append(resourceName)
    
    for resourceName in resourceNameList:
        rLineEssence = RLineEssence.ResourceLineEssence(oLineData,resourceName)
        rLineEssence.Output(pathData.GetPath())
        rLineData = RLineData.ResourceLineData(rLineEssence)
        rLineData.Output(pathData.GetPath())
        rlineDoc = RLineDoc.ResourceLineDocument()
        rlineDoc.MakeDocument(pathData,rLineData)
    


# 個別製造ライン設計書作成
iLineEssences = oDesignMaker.individualLineEssences
iLineDataList = []
for iLineEssence in iLineEssences:
    iDesignMaker = MakeIndividualLineDesign.IndividualLineDesignMaker()
    iLineData = iDesignMaker.Main(pathData,iLineEssence)
    iLineDataList.append(iLineData)



# 個別製造ラインテスト項目書作成
for iLineData in iLineDataList:
    checkListMaker = MakeIndividualLineCheckList.MakeIndividualLineCheckList()
    checkListMaker.Main(pathData,iLineData)


# 工場データ出力
FactoryDataOutputModule.OutputFactoryData(pathData, oLineData, iLineDataList)
