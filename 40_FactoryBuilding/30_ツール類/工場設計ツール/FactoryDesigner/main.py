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
iDesignMaker = MakeIndividualLineDesign.IndividualLineDesignMaker()
iDesignMaker.Main(pathData)

# 個別製造ラインテスト項目書作成
checkListMaker = MakeIndividualLineCheckList.MakeIndividualLineCheckList()
checkListMaker.Main(pathData)