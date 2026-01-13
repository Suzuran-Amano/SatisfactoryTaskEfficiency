import os

from . import pathDataModule
from . import InfomationReaderModule as InfoReader
from . import RecipeItemModule
from . import ResourceLineDataModule as RLineDataModule
from . import DocumentMakerModule 


# 資源産出ライン設計書を作成、出力するクラス
class ResourceLineDocument(DocumentMakerModule.DocumentMaker):
    
    # 定数
    TEMPLATE_FILE_NAME = '資源産出ライン設計書_var_lineName.md'
    OUTPUT_FILE_NAME = '資源産出ライン設計書_var_lineName.md'


    # 書類の作成と出力を行う関数
    def MakeDocument(
            self,
            pathData : pathDataModule.PathData,
            rLineData : RLineDataModule.ResourceLineData
            ):

        # テンプレートの読み込みと置換
        lines = self._ReadTemplateFile(self.TEMPLATE_FILE_NAME)
        lines = self._DuplicateResourceLines(lines,rLineData)
        lines = self._AllLineReplace(lines,rLineData)

        # 書類の出力
        self._WriteFile(pathData,rLineData, lines)

        return


    # 置き換え
    def _AllLineReplace(
            self,
            lines : list,
            rLineData : RLineDataModule.ResourceLineData
            ) -> list:

        replaceDict = rLineData.GetValueDict()

        resourceList = rLineData.GetValue(RLineDataModule.RESOURCE_LIST_KEY)
        for i in range(len(resourceList)):
            # 資源倍率
            replaceKey = RLineDataModule.RESOURCE_RATIO_KEY + str(i+1)
            value = resourceList[i][RLineDataModule.RESOURCE_RATIO_KEY]
            replaceDict[replaceKey] = value
            
            # 設備名
            replaceKey = RLineDataModule.BUILDING_NAME_KEY + str(i+1)
            value = resourceList[i][RLineDataModule.BUILDING_NAME_KEY]
            replaceDict[replaceKey] = value
            
            # オーバークロック倍率
            replaceKey = RLineDataModule.OVERCLOCK_RATIO_KEY + str(i+1)
            value = resourceList[i][RLineDataModule.OVERCLOCK_RATIO_KEY]
            replaceDict[replaceKey] = value

        lines = super()._AllLineReplace(lines,replaceDict)

        return lines

    # 保存
    def _WriteFile(
            self,
            pathData : pathDataModule.PathData,
            rLineData : RLineDataModule.ResourceLineData,
            lines : list
            ):

        outputPath = pathData.GetPath() + "\\" + pathDataModule.INDIVIDUAL_LINE_DIRECTORY_NAME
        fileName = self._Replace(self.OUTPUT_FILE_NAME,rLineData.GetValueDict())

        super()._WriteFile(outputPath,fileName,lines)

        return


    # 資産の数分を複製する
    def _DuplicateResourceLines(
            self,
            lines,
            rLineData : RLineDataModule.ResourceLineData
            ):
        
        length = len(rLineData.GetValue(RLineDataModule.RESOURCE_LIST_KEY))
        keys = []
        keys.append(self._GetReplaceKey(RLineDataModule.RESOURCE_RATIO_KEY))
        keys.append(self._GetReplaceKey(RLineDataModule.BUILDING_NAME_KEY))
        keys.append(self._GetReplaceKey(RLineDataModule.OVERCLOCK_RATIO_KEY))

        return self._DuplicateLines(lines,length,keys)