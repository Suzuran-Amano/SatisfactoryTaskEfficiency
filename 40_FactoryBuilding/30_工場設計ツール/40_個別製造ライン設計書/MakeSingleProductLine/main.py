import sys

from MakeIndividualLineDesignModules import pathDataModule
import MakeIndividualLineDesign
import MakeIndividualLineCheckList


# パス情報を作成
pathData = pathDataModule.PathData(sys.argv)

# 個別製造ライン設計書作成
designMaker = MakeIndividualLineDesign.IndividualLineDesignMaker()
designMaker.Main(pathData)

# 個別製造ラインテスト項目書作成
checkListMaker = MakeIndividualLineCheckList.MakeIndividualLineCheckList()
checkListMaker.Main(pathData)