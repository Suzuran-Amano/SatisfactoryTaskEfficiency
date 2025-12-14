import sys

from MakeIndividualLineDesignModules import pathDataModule
import MakeIndividualLineDesign
import MakeIndividualLineCheckList


pathData = pathDataModule.PathData(sys.argv)
print(pathData.GetFileName())
print(pathData.GetFilePath())

# 個別製造ライン設計書作成
designMaker = MakeIndividualLineDesign.IndividualLineDesignMaker()
designMaker.Main(sys.argv)

# 個別製造ラインテスト項目書作成
checkListMaker = MakeIndividualLineCheckList.MakeIndividualLineCheckList()
checkListMaker.Main(sys.argv)