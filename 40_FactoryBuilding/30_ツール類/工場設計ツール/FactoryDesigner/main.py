import sys

from DesignModules import pathDataModule
import MakeOverallLineDesign
import MakeIndividualLineDesign
import MakeIndividualLineCheckList


# パス情報を作成
pathData = pathDataModule.PathData(sys.argv)

# 全体製造ライン設計書作成
oDesignMaker = MakeOverallLineDesign.OverallLineDesignMaker()
oDesignMaker.Main(pathData)


# 個別製造ライン設計書作成
iLines = oDesignMaker.individualLineEssences
for iLine in iLines:
    iDesignMaker = MakeIndividualLineDesign.IndividualLineDesignMaker()
    iDesignMaker.Main(pathData,iLine)

# 個別製造ラインテスト項目書作成
for iLine in iLines:
    checkListMaker = MakeIndividualLineCheckList.MakeIndividualLineCheckList()
    checkListMaker.Main(pathData,iLine)