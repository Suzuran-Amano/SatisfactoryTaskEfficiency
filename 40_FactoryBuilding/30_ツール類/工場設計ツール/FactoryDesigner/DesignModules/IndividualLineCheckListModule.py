import os

from . import pathDataModule
from . import InfomationReaderModule as InfoReader
from . import RecipeItemModule
from . import IndividualLineDataModule as ILineDataModule
from . import DocumentMakerModule 


# 個別造製ライン設計書を作成、出力するクラス
class IndividualLineCheckList(DocumentMakerModule.DocumentMaker):

    # 定数
    TEMPLATE_FILE_NAME = '個別製造ラインテスト項目書_var_lineName.md'
    OUTPUT_FILE_NAME = '個別製造ラインテスト項目書_var_lineName.md'


    # 書類の作成と出力を行う関数
    def MakeDocument(
            self,
            pathData : pathDataModule.PathData,
            iLineData : ILineDataModule.IndividualLineData
            ):
        
        # 使用するデータの読み込み
        recipeData = InfoReader.GetRecipe(iLineData.GetValue(ILineDataModule.RECIPE_NAME_KEY))

        # テンプレートの読み込みと置換
        lines = self._ReadTemplateFile(self.TEMPLATE_FILE_NAME)
        lines = self._DuplicateProductItem(lines,iLineData)
        lines = self._DuplicateInputLines(lines,recipeData)
        lines = self._DuplicateOutputLines(lines,recipeData)
        lines = self._AllLineReplace(lines,iLineData.GetValueDict())

        # 書類の出力
        self._WriteFile(pathData,iLineData, lines)

        return


    # 保存
    def _WriteFile(
            self,
            pathData : pathDataModule.PathData,
            iLineData : ILineDataModule.IndividualLineData,
            lines : list
            ):

        outputPath = pathData.GetPath() + "\\" + pathDataModule.INDIVIDUAL_TEST_DIRECTORY_NAME
        fileName = self._Replace(self.OUTPUT_FILE_NAME,iLineData.GetValueDict())

        super()._WriteFile(outputPath,fileName,lines)

        return


    # 複数の Product を記載するため、行を複製
    def _DuplicateProductItem(
            self,
            lines,
            recipeItem : RecipeItemModule.RecipeItem
            ):

        length = recipeItem.GetValue(ILineDataModule.RECIPE_NUM_KEY)
        keys = []
        keys.append(self._GetReplaceKey(ILineDataModule.PRODUCT_NAME_KEY))

        return self._DuplicateLines(lines,length,keys)
    
    
    # 供給物品の数分を複製する
    def _DuplicateInputLines(
            self,
            lines,
            recipeItem : RecipeItemModule.RecipeItem
            ):
        
        length = len(recipeItem.GetValue(RecipeItemModule.INPUT_KEY))
        keys = []
        keys.append(self._GetReplaceKey(ILineDataModule.INPUT_NAME_KEY))
        keys.append(self._GetReplaceKey(ILineDataModule.INPUT_NUM_KEY))
        keys.append(self._GetReplaceKey(ILineDataModule.TOTAL_INPUT_KEY))

        return self._DuplicateLines(lines,length,keys)
    
    
    # 出力物品の数分を複製する
    def _DuplicateOutputLines(
            self,
            lines,
            recipeItem : RecipeItemModule.RecipeItem
            ):
        
        length = len(recipeItem.GetValue(RecipeItemModule.OUTPUT_KEY))
        keys = []
        keys.append(self._GetReplaceKey(ILineDataModule.OUTPUT_NAME_KEY))
        keys.append(self._GetReplaceKey(ILineDataModule.OUTPUT_NUM_KEY))
        keys.append(self._GetReplaceKey(ILineDataModule.TOTAL_OUTPUT_KEY))

        return self._DuplicateLines(lines,length,keys)


    # 物品の数分を複製する
    def _DuplicateLines(
            self,
            lines,
            length : int,
            keys : list
            ):
        
        resultLines = []

        # 複製
        for line in lines:
            
            # 複製する必要があるかを判定
            shouldReplace = False
            for key in keys:
                if key in line:
                    shouldReplace = True
                    break
            
            # 複製する必要が無かったら
            if not(shouldReplace):
                resultLines.append(line)
                continue


            # 複製する必要があるなら
            for f in range(length):
                newLine = line
                for key in keys:
                    newLine = newLine.replace(key, key + str(f+1))
                resultLines.append(newLine)

        return resultLines
    

