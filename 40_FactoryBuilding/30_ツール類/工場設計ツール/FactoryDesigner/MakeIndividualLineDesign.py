import os
import json

from DesignModules import InfomationReaderModule as InfoReader
from DesignModules import RecipeItemModule as RecipeItem
from DesignModules import IndividualLineEssenceModule as ILineEssence
from DesignModules import IndividualLineDataModule as ILineData
from DesignModules import IndividualLineDocumentModule as ILineDoc
from DesignModules import pathDataModule

# 個別製造ライン設計書作成用クラス
class IndividualLineDesignMaker:

    inputNum = 0
    outputNum = 0


    def Main(
            self,
            pathData : pathDataModule.PathData,
            iLineEssence : ILineEssence.IndividualLineEssence
            ) -> ILineData.IndividualLineData:
        
        # 置換用データを作成
        individualLineData = ILineData.IndividualLineData(iLineEssence)
        individualLineData.Output(pathData.GetPath())
        
        # 個別ライン設計書を出力
        ILineDoc.IndividualLineDocument(pathData,individualLineData)

        return individualLineData

