import os
import json

from DesignModules import InfomationReaderModule as InfoReader
from DesignModules import RecipeItemModule as RecipeItem
from DesignModules import BuildingDataManagerModule as BuildingData
from DesignModules import IndividualLineEssenceModule as ILineEssence
from DesignModules import IndividualLineDataModule as ILineData
from DesignModules import pathDataModule

# 個別製造ライン設計書作成用クラス
class IndividualLineDesignMaker:

    # constans
    inputTextFileName = './個別製造ライン設計書_var_lineName.md'
    inputDataFileName = './IndividualLine.json'
    outputFileName = '個別製造ライン設計書_var_lineName.md'
    


    inputNum = 0
    outputNum = 0


    def Main(
            self,
            pathData : pathDataModule.PathData,
            iLineEssence : ILineEssence.IndividualLineEssence
            ) -> ILineData.IndividualLineData:

        # input file read
        templateLines = self.ReadTemplateFile()
        recipeData = InfoReader.GetRecipe(iLineEssence.GetValue(ILineEssence.RECIPE_NAME_KEY))
        buildingData = InfoReader.GetBuildingData(recipeData.GetValue(RecipeItem.PRODUCT_NAME_KEY))
        
        # 置換用データを作成
        individualLineData = self.MakeIndividualLineData(iLineEssence,recipeData,buildingData)
        individualLineData.Output(pathData.GetPath())
        

        # MakeFlowChart
        insertNum = 0
        for index, item in enumerate(templateLines):
            if item == "## 製造ライン":
                insertNum = index + 1
                break

        flowChart = self.MakeFlowChart(individualLineData)

        for chartLine in flowChart:
            templateLines.insert(insertNum,chartLine)
            insertNum += 1


        # replace
        templateLines = self.DuplicateInputItem(templateLines,recipeData,individualLineData)
        templateLines = self.DuplicateOutputItem(templateLines,recipeData,individualLineData)
        for index, item in enumerate(templateLines):
            templateLines[index] = self.Replace(templateLines[index],individualLineData)


        # text output
        filePath = pathData.GetPath() + "\\" + pathDataModule.INDIVIDUAL_LINE_DIRECTORY_NAME
        fileName = self.Replace(self.outputFileName,individualLineData)
        self.WriteFile(filePath,fileName,templateLines)

        return individualLineData


    # テンプレートファイルを読み込み
    def ReadTemplateFile(self):
        lines = []
        os.chdir(os.path.dirname(__file__) + "/../")
        with open(self.inputTextFileName, encoding="utf-8") as f:
            for line in f:
                lines.append(line.rstrip())
        return lines


    # 個別ライン本質ファイルを読み込み
    def ReadIndividualLineFile(self,inputDataFileName):
        jsonData = json.load(open(inputDataFileName,'r', encoding="utf-8"))
        individualLine = ILineEssence.IndividualLineEssence(jsonData)
        return individualLine

  

    # 保存
    def WriteFile(self,filePath,fileName,lines):
        os.chdir(os.path.dirname(__file__) + "/../")
        os.chdir(filePath)
        with open(fileName,"w", encoding="utf-8") as o:
            for line in lines:
                print(line,file=o)
        return


    # 個別ラインデータを作成
    def MakeIndividualLineData(
            self,
            iLineEssence : ILineEssence.IndividualLineEssence,
            recipeItem : RecipeItem.RecipeItem,
            buildingData):
        
        iLineData = ILineData.IndividualLineData()

        # ライン名を追加
        iLineData.Append(
            ILineData.LINE_NAME_KEY,
            iLineEssence.GetValue(ILineEssence.LINE_NAME_KEY))

        # レシピ名を追加
        iLineData.Append(ILineData.RECIPE_NAME_KEY,recipeItem.GetValue(RecipeItem.RECIPE_NAME_KEY))
        recipeNum = iLineEssence.GetValue(ILineEssence.RECIPE_NUM_KEY)
        iLineData.Append(ILineData.RECIPE_NUM_KEY,recipeNum)

        # 制作物を追加
        productName = recipeItem.GetValue(RecipeItem.PRODUCT_NAME_KEY)
        iLineData.Append(ILineData.PRODUCT_NAME_KEY,productName)

        # 合計コストを追加
        buildingData = InfoReader.GetBuildingData(productName)
        costList = []
        for cost in buildingData.GetValue(BuildingData.COST_KEY):
            costList.append({
                ILineData.ITEM_NAME_KEY : cost[BuildingData.ITEM_NAME_KEY],
                ILineData.ITEM_NUM_KEY : cost[BuildingData.ITEM_NUM_KEY] * recipeNum

            })
        iLineData.Append(ILineData.COST_LIST_KEY,costList)

        # 合計消費電力を追加
        totalUsePower = buildingData.GetValue(BuildingData.USE_POWER_KEY) * recipeNum
        iLineData.Append(ILineData.TOTAL_USE_POWER_KEY,totalUsePower)

        # 搬入物を追加
        index = 0
        for data in recipeItem.GetValue(RecipeItem.INPUT_KEY):
            inputNameKey = ILineData.INPUT_NAME_KEY + str(index+1)
            inputName = data[RecipeItem.ITEM_NAME_KEY]
            iLineData.Append(inputNameKey, inputName)
            
            inputNumKey = ILineData.INPUT_NUM_KEY + str(index+1)
            inputNum = data[RecipeItem.ITEM_NUM_KEY]
            iLineData.Append(inputNumKey ,inputNum)
            
            inputTotalKey = ILineData.TOTAL_INPUT_KEY + str(index+1)
            inputTotal = recipeNum*inputNum
            iLineData.Append(inputTotalKey,inputTotal)
            
            index = index + 1
        
        # 搬出物を追加
        index = 0
        for data in recipeItem.GetValue(RecipeItem.OUTPUT_KEY):
            outputNameKey = ILineData.OUTPUT_NAME_KEY + str(index+1)
            outputName = data[RecipeItem.ITEM_NAME_KEY]
            iLineData.Append(outputNameKey, outputName)
            
            outputNumKey = ILineData.OUTPUT_NUM_KEY + str(index+1)
            outputNum = data[RecipeItem.ITEM_NUM_KEY]
            iLineData.Append(outputNumKey ,outputNum)
            
            outputTotalKey = ILineData.TOTAL_OUTPUT_KEY + str(index+1)
            outputTotal = recipeNum*outputNum
            iLineData.Append(outputTotalKey,outputTotal)

            index = index + 1

        # 供給電力を追加
        supplyPower = recipeItem.GetValue(RecipeItem.SUPPLY_POWER_KEY)
        if supplyPower == None:
            supplyPower = 0
        supplyPower = supplyPower * recipeNum
        iLineData.Append(ILineData.SUPPLY_POWER_KEY,supplyPower)

                    
        return iLineData


    # 置き換え
    def Replace(
            self,
            text : str,
            iLineData : ILineData.IndividualLineData
            ):
        
        for key in iLineData.GetKeys():
            text = text.replace(iLineData.GetReplaceKey(key),str(iLineData.GetValue(key)))
        return text
    
    
    # 複数の Input 物品を記載するため、行を複製
    def DuplicateInputItem(
            self,
            templateLines,
            recipeItem : RecipeItem.RecipeItem,
            iLineData : ILineData.IndividualLineData
            ):
        
        resultLines = []
        inputLength = len(recipeItem.GetValue(RecipeItem.INPUT_KEY))

        inputNameKey = ILineData.INPUT_NAME_KEY
        inputReplaceNameKey = iLineData.GetReplaceKey(inputNameKey)
        
        inputNumKey = ILineData.INPUT_NUM_KEY
        inputReplaceNumKey = iLineData.GetReplaceKey(inputNumKey)

        inputTotalKey = ILineData.TOTAL_INPUT_KEY
        inputReplaceTotalKey = iLineData.GetReplaceKey(inputTotalKey)
        
        for i in range(len(templateLines)):
            if not(ILineData.INPUT_NAME_KEY in templateLines[i]):
                resultLines.append(templateLines[i])
                continue
            
            for f in range(inputLength):
                line = templateLines[i].replace(inputReplaceNameKey, inputReplaceNameKey + str(f+1))
                line = line.replace(inputReplaceNumKey, inputReplaceNumKey + str(f+1))
                line = line.replace(inputReplaceTotalKey, inputReplaceTotalKey + str(f+1))
                resultLines.append(line)

        return resultLines
        
    
    # 複数の Output 物品を記載するため、行を複製
    def DuplicateOutputItem(
            self,
            templateLines,
            recipeItem : RecipeItem.RecipeItem,
            iLineData :ILineData.IndividualLineData
            ):
        

        resultLines = []
        outputLength = len(recipeItem.GetValue(RecipeItem.OUTPUT_KEY))

        outputNameKey = ILineData.OUTPUT_NAME_KEY
        outputReplaceNameKey = iLineData.GetReplaceKey(outputNameKey)
        
        outputNumKey = ILineData.OUTPUT_NUM_KEY
        outputReplaceNumKey = iLineData.GetReplaceKey(outputNumKey)

        outputTotalKey = ILineData.TOTAL_OUTPUT_KEY
        outputReplaceTotalKey = iLineData.GetReplaceKey(outputTotalKey)
        
        for i in range(len(templateLines)):
            if not(ILineData.OUTPUT_NAME_KEY in templateLines[i]):
                resultLines.append(templateLines[i])
                continue
            
            for f in range(outputLength):
                line = templateLines[i].replace(outputReplaceNameKey, outputReplaceNameKey + str(f+1))
                line = line.replace(outputReplaceNumKey, outputReplaceNumKey + str(f+1))
                line = line.replace(outputReplaceTotalKey, outputReplaceTotalKey + str(f+1))
                resultLines.append(line)

        return resultLines


    def MakeFlowChart(
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


