import os

from . import RecipeItemModule
from . import pathDataModule
from . import InfomationReaderModule as InfoReader
from . import RecipeItemModule as RecipeItem
from . import IndividualLineDataModule as ILineData

# 個別ライン設計書を管理するクラス
class IndividualLineDocument():
    
    # constans
    TEMPLATE_FILE_NAME = '個別製造ライン設計書_var_lineName.md'
    inputDataFileName = 'IndividualLine.json'
    outputFileName = '個別製造ライン設計書_var_lineName.md'


    def __init__(
            self,
            pathData : pathDataModule.PathData,
            iLineData : ILineData.IndividualLineData
            ):
        
        recipeData = InfoReader.GetRecipe(iLineData.GetValue(ILineData.RECIPE_NAME_KEY))

        lines = self._ReadTemplateFile()
        lines = self._MakeFlowChart(lines,iLineData)
        lines = self._DuplicateInputLines(lines,recipeData,iLineData)
        lines = self._DuplicateOutputLines(lines,recipeData,iLineData)
        for index in range(len(lines)):
            lines[index] = self._Replace(lines[index],iLineData)


         # text output
        self._WriteFile(pathData,iLineData, lines)

        return


    # テンプレートファイルを読み込み
    def _ReadTemplateFile(self):
        lines = []
        
        abs_path = os.path.abspath(__file__)
        dir_path = os.path.dirname(abs_path)
        filePath = dir_path + "\\" + self.TEMPLATE_FILE_NAME
        with open(filePath, encoding="utf-8") as f:
            for line in f:
                lines.append(line.rstrip())
        return lines
  

    # 保存
    def _WriteFile(
            self,
            pathData : pathDataModule.PathData,
            iLineData : ILineData.IndividualLineData,
            lines):

        outputPath = pathData.GetPath() + "\\" + pathDataModule.INDIVIDUAL_LINE_DIRECTORY_NAME
        fileName = self._Replace(self.outputFileName,iLineData)

        os.makedirs(outputPath, exist_ok=True)
        with open(outputPath + "\\" + fileName , "w", encoding="utf-8") as o:
            for line in lines:
                print(line,file=o)
        return


    # 置き換え
    def _Replace(
            self,
            text : str,
            iLineData : ILineData.IndividualLineData
            ):
        
        for key in iLineData.GetKeys():
            text = text.replace(iLineData.GetReplaceKey(key),str(iLineData.GetValue(key)))

        return text
    
    # 供給物品の数分を複製する
    def _DuplicateInputLines(
            self,
            lines,
            recipeItem : RecipeItemModule.RecipeItem,
            iLineData :ILineData.IndividualLineData
            ):
        
        length = len(recipeItem.GetValue(RecipeItemModule.INPUT_KEY))
        keys = []
        keys.append(iLineData.GetReplaceKey(ILineData.INPUT_NAME_KEY))
        keys.append(iLineData.GetReplaceKey(ILineData.INPUT_NUM_KEY))
        keys.append(iLineData.GetReplaceKey(ILineData.TOTAL_INPUT_KEY))

        return self._DuplicateLines(lines,length,keys)
    
    
    # 出力物品の数分を複製する
    def _DuplicateOutputLines(
            self,
            lines,
            recipeItem : RecipeItemModule.RecipeItem,
            iLineData :ILineData.IndividualLineData
            ):
        
        length = len(recipeItem.GetValue(RecipeItemModule.OUTPUT_KEY))
        keys = []
        keys.append(iLineData.GetReplaceKey(ILineData.OUTPUT_NAME_KEY))
        keys.append(iLineData.GetReplaceKey(ILineData.OUTPUT_NUM_KEY))
        keys.append(iLineData.GetReplaceKey(ILineData.TOTAL_OUTPUT_KEY))

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
    

    def _MakeFlowChart(
            self,
            templateLines,
            iLineData : ILineData.IndividualLineData
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
            iLineData : ILineData.IndividualLineData
            ):

        result = []
        inputName = iLineData.GetReplaceKey(ILineData.INPUT_NAME_KEY)
        inputNum = iLineData.GetReplaceKey(ILineData.INPUT_NUM_KEY)
        outputName = iLineData.GetReplaceKey(ILineData.OUTPUT_NAME_KEY)
        outputNum = iLineData.GetReplaceKey(ILineData.OUTPUT_NUM_KEY)
        productName = iLineData.GetReplaceKey(ILineData.PRODUCT_NAME_KEY)
        productNum = iLineData.GetValue(ILineData.RECIPE_NUM_KEY)
            
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


