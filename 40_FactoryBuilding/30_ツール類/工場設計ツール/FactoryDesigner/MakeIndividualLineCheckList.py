from DesignModules import IndividualLineDataModule as ILineData
from DesignModules import IndividualLineCheckListModule as ILineCheckList
from DesignModules import pathDataModule


# 個別製造ラインテスト項目書作成
class MakeIndividualLineCheckList:

    inputNum = 0
    outputNum = 0


    def Main(self,
            pathData : pathDataModule.PathData,
            iLineData : ILineData.IndividualLineData
            ):

        ILineCheckList.IndividualLineCheckList().MakeDocument(pathData,iLineData)

        return


