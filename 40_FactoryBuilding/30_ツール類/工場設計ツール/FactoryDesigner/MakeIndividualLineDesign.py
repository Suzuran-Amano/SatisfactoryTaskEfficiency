import os
import json

from DesignModules import RecipeReaderModule as RecipeReader
from DesignModules import RecipeItemModule as RecipeItem
from DesignModules import BuildingDataManagerModule
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
        recipeData = RecipeReader.GetRecipe(iLineEssence.GetValue(ILineEssence.RECIPE_NAME_KEY))
        buildingData = self.ReadBuildingInfoFile(recipeData)
        
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


    # 設備データを読み込み
    def ReadBuildingInfoFile(self,recipe:RecipeItem) -> BuildingDataManagerModule.BuildingDataItem:
        buildingInfo = BuildingDataManagerModule.BuildingDataReader()
        buildingInfo = buildingInfo.GetBuildingInfo(recipe.GetProductName())
        return buildingInfo
    

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
            recipeData,
            buildingData):
        
        iLineData = ILineData.IndividualLineData()

        # ライン名を追加
        iLineData.Append(
            iLineData.LINE_NAME_KEY,
            iLineEssence.GetValue(ILineEssence.LINE_NAME_KEY))

        # レシピ名を追加
        iLineData.Append(iLineData.RECIPE_NAME_KEY,recipeData.GetRecipeName())
        recipeNum = iLineEssence.GetValue(ILineEssence.RECIPE_NUM_KEY)
        iLineData.Append(iLineData.RECIPE_NUM_KEY,recipeNum)

        # 制作物を追加
        productName = recipeData.GetProductName()
        iLineData.Append(iLineData.PRODUCT_NAME_KEY,productName)

        # 合計コストを追加
        buildingReader = BuildingDataManagerModule.BuildingDataReader()
        buildingData = buildingReader.GetBuildingData(productName)
        costList = []
        for cost in buildingData.GetCostList():
            costList.append({
                iLineData.ITEM_NAME_KEY : cost[buildingData.ITEM_NAME_KEY],
                iLineData.ITEM_NUM_KEY : cost[buildingData.ITEM_NUM_KEY] * recipeNum

            })
        iLineData.Append(iLineData.COST_LIST_KEY,costList)

        # 合計消費電力を追加
        totalUsePower = buildingData.GetUsePower() * recipeNum
        iLineData.Append(iLineData.TOTAL_USE_POWER_KEY,totalUsePower)

        # 搬入物を追加
        index = 0
        for data in recipeData.GetInputItemList():
            inputNameKey = iLineData.INPUT_NAME_KEY + str(index+1)
            inputName = data[RecipeItem.ITEM_NAME_KEY]
            iLineData.Append(inputNameKey, inputName)
            
            inputNumKey = iLineData.INPUT_NUM_KEY + str(index+1)
            inputNum = data[RecipeItem.ITEM_NUM_KEY]
            iLineData.Append(inputNumKey ,inputNum)
            
            inputTotalKey = iLineData.TOTAL_INPUT_KEY + str(index+1)
            inputTotal = recipeNum*inputNum
            iLineData.Append(inputTotalKey,inputTotal)
            
            index = index + 1
        
        # 搬出物を追加
        index = 0
        for data in recipeData.GetOutputItemList():
            outputNameKey = iLineData.OUTPUT_NAME_KEY + str(index+1)
            outputName = data[RecipeItem.ITEM_NAME_KEY]
            iLineData.Append(outputNameKey, outputName)
            
            outputNumKey = iLineData.OUTPUT_NUM_KEY + str(index+1)
            outputNum = data[RecipeItem.ITEM_NUM_KEY]
            iLineData.Append(outputNumKey ,outputNum)
            
            outputTotalKey = iLineData.TOTAL_OUTPUT_KEY + str(index+1)
            outputTotal = recipeNum*outputNum
            iLineData.Append(outputTotalKey,outputTotal)

            index = index + 1

        # 供給電力を追加
        supplyPower = recipeData.GetSupplyPower() * recipeNum
        iLineData.Append(iLineData.SUPPLY_POWER_KEY,supplyPower)

                    
        return iLineData


    # 置き換え
    def Replace(self,text,iLineData):
        for key in iLineData.GetKeys():
            text = text.replace(iLineData.GetReplaceKey(key),str(iLineData.value[key]))
        return text
    
    
    # 複数の Input 物品を記載するため、行を複製
    def DuplicateInputItem(self,templateLines,recipeData,iLineData):
        resultLines = []
        inputLength = int(recipeData.GetInputItemLength())

        inputNameKey = iLineData.INPUT_NAME_KEY
        inputReplaceNameKey = iLineData.GetReplaceKey(inputNameKey)
        
        inputNumKey = iLineData.INPUT_NUM_KEY
        inputReplaceNumKey = iLineData.GetReplaceKey(inputNumKey)

        inputTotalKey = iLineData.TOTAL_INPUT_KEY
        inputReplaceTotalKey = iLineData.GetReplaceKey(inputTotalKey)
        
        for i in range(len(templateLines)):
            if not(iLineData.INPUT_NAME_KEY in templateLines[i]):
                resultLines.append(templateLines[i])
                continue
            
            for f in range(inputLength):
                line = templateLines[i].replace(inputReplaceNameKey, inputReplaceNameKey + str(f+1))
                line = line.replace(inputReplaceNumKey, inputReplaceNumKey + str(f+1))
                line = line.replace(inputReplaceTotalKey, inputReplaceTotalKey + str(f+1))
                resultLines.append(line)

        return resultLines
        
    
    # 複数の Output 物品を記載するため、行を複製
    def DuplicateOutputItem(self,templateLines,recipeData,iLineData):
        resultLines = []
        outputLength = int(recipeData.GetOutputItemLength())

        outputNameKey = iLineData.OUTPUT_NAME_KEY
        outputReplaceNameKey = iLineData.GetReplaceKey(outputNameKey)
        
        outputNumKey = iLineData.OUTPUT_NUM_KEY
        outputReplaceNumKey = iLineData.GetReplaceKey(outputNumKey)

        outputTotalKey = iLineData.TOTAL_OUTPUT_KEY
        outputReplaceTotalKey = iLineData.GetReplaceKey(outputTotalKey)
        
        for i in range(len(templateLines)):
            if not(iLineData.OUTPUT_NAME_KEY in templateLines[i]):
                resultLines.append(templateLines[i])
                continue
            
            for f in range(outputLength):
                line = templateLines[i].replace(outputReplaceNameKey, outputReplaceNameKey + str(f+1))
                line = line.replace(outputReplaceNumKey, outputReplaceNumKey + str(f+1))
                line = line.replace(outputReplaceTotalKey, outputReplaceTotalKey + str(f+1))
                resultLines.append(line)

        return resultLines


    def MakeFlowChart(self,iLineData):

        result = []
        inputName = iLineData.GetReplaceKey(iLineData.INPUT_NAME_KEY)
        inputNum = iLineData.GetReplaceKey(iLineData.INPUT_NUM_KEY)
        outputName = iLineData.GetReplaceKey(iLineData.OUTPUT_NAME_KEY)
        outputNum = iLineData.GetReplaceKey(iLineData.OUTPUT_NUM_KEY)
        productName = iLineData.GetReplaceKey(iLineData.PRODUCT_NAME_KEY)
        productNum = iLineData.GetRecipeNum()
            
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


