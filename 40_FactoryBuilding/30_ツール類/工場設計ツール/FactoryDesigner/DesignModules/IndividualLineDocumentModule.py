import os

from . import pathDataModule
from .BasicData import BasicDataReader
from .BasicData import RecipeData
from . import IndividualLineDataModule as ILineDataModule
from . import DocumentMakerModule 


# 個別造製ライン設計書を作成、出力するクラス
class IndividualLineDocument(DocumentMakerModule.DocumentMaker):
    
    # 定数
    TEMPLATE_FILE_NAME = '個別製造ライン設計書_var_lineName.md'
    OUTPUT_FILE_NAME = '個別製造ライン設計書_var_lineName.md'


    # 書類の作成と出力を行う関数
    def MakeDocument(
            self,
            pathData : pathDataModule.PathData,
            iLineData : ILineDataModule.IndividualLineData
            ):
                
        # 使用するデータの読み込み
        recipeData = BasicDataReader.GetRecipe(iLineData.GetValue(ILineDataModule.RECIPE_NAME_KEY))

        # テンプレートの読み込みと置換
        lines = self._ReadTemplateFile(self.TEMPLATE_FILE_NAME)
        lines = self._MakeFlowChart(lines,iLineData)
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

        outputPath = pathData.GetPath() + "\\" + pathDataModule.INDIVIDUAL_LINE_DIRECTORY_NAME
        fileName = self._Replace(self.OUTPUT_FILE_NAME,iLineData.GetValueDict())

        super()._WriteFile(outputPath,fileName,lines)

        return


    # 供給物品の数分を複製する
    def _DuplicateInputLines(
            self,
            lines,
            recipeData : RecipeData.RecipeData
            ):
        
        length = len(recipeData.GetValue(RecipeData.INPUT_KEY))
        keys = []
        keys.append(self._GetReplaceKey(ILineDataModule.INPUT_NAME_KEY))
        keys.append(self._GetReplaceKey(ILineDataModule.INPUT_NUM_KEY))
        keys.append(self._GetReplaceKey(ILineDataModule.TOTAL_INPUT_KEY))

        return self._DuplicateLines(lines,length,keys)
    
    
    # 出力物品の数分を複製する
    def _DuplicateOutputLines(
            self,
            lines,
            recipeData : RecipeData.RecipeData
            ):
        
        length = len(recipeData.GetValue(RecipeData.OUTPUT_KEY))
        keys = []
        keys.append(self._GetReplaceKey(ILineDataModule.OUTPUT_NAME_KEY))
        keys.append(self._GetReplaceKey(ILineDataModule.OUTPUT_NUM_KEY))
        keys.append(self._GetReplaceKey(ILineDataModule.TOTAL_OUTPUT_KEY))

        return self._DuplicateLines(lines,length,keys)
    

    def _MakeFlowChart(
            self,
            templateLines,
            iLineData : ILineDataModule.IndividualLineData
            ):

        # MakeFlowChart
        insertNum = 0
        for index, item in enumerate(templateLines):
            if item == "## 製造ライン":
                insertNum = index + 1
                break

        flowChart = self._MakeFlowChartMarmaid(iLineData)

        for chartLine in flowChart:
            templateLines.insert(insertNum,chartLine)
            insertNum += 1
        
        return templateLines


    def _MakeFlowChartMarmaid(
            self,
            iLineData : ILineDataModule.IndividualLineData
            ):

        result = []
        inputName = self._GetReplaceKey(ILineDataModule.INPUT_NAME_KEY)
        inputNum = self._GetReplaceKey(ILineDataModule.INPUT_NUM_KEY)
        outputName = self._GetReplaceKey(ILineDataModule.OUTPUT_NAME_KEY)
        outputNum = self._GetReplaceKey(ILineDataModule.OUTPUT_NUM_KEY)
        productName = self._GetReplaceKey(ILineDataModule.PRODUCT_NAME_KEY)
        productNum = iLineData.GetValue(ILineDataModule.RECIPE_NUM_KEY)
            
        # header
        result.append("```mermaid")
        result.append("flowchart TD\n")

        # input
        result.append("subgraph Input")
        result.append("    " + inputName +"([" + inputName + "])")
        result.append("end\n")

        # product
        for i in range(productNum):

            result.append(productName + str(i+1) + "[")
            result.append("    " + productName + str(i+1))
            result.append("    " + inputName + " " + str(inputNum) + "/m")
            result.append("    ↓")
            result.append("    " + outputName + " " + str(outputNum) + "/m" )
            result.append("]\n")

        # output
        result.append("subgraph Output")
        result.append("    " + outputName +"([" + outputName + "])")
        result.append("end\n")


        for i in range(productNum):

            result.append(inputName + "-->|" + str(inputNum) + "|" + productName + str(i+1))
            result.append(productName + str(i+1) + "-->|" + str(outputNum) + "|" + outputName)

        result.append("```\n")
        
        return result


