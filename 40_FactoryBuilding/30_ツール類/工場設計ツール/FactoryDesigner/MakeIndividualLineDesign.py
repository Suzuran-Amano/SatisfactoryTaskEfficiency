import os
import json

from DesignModules import recipeManagerModule
from DesignModules import BuildingDataManagerModule
from DesignModules import IndividualLineEssenceModule
from DesignModules import IndividualLineDataModule
from DesignModules import pathDataModule

# 個別製造ライン設計書作成用クラス
class IndividualLineDesignMaker:

    # constans
    INDIVIDUAL_LINE_DIRECTORY_NAME = "40_個別製造ライン設計書"

    inputTextFileName = './個別製造ライン設計書_var_lineName.md'
    inputDataFileName = './IndividualLine.json'
    outputFileName = '個別製造ライン設計書_var_lineName.md'
    


    inputNum = 0
    outputNum = 0


    def Main(
            self,
            pathData : pathDataModule.PathData,
            iLineData : IndividualLineEssenceModule.IndividualLineEssence
            ) -> IndividualLineDataModule.IndividualLineData:

        # ファイルのフルパスを取得
        inputDataFileName = pathData.GetPath() + "/" + self.inputDataFileName

        # input file read
        templateLines = self.ReadTemplateFile()
        individualLine = iLineData
        recipeData = self.ReadRecipeFile(individualLine)
        buildingData = self.ReadBuildingInfoFile(recipeData)
        
        # 置換用データを作成
        individualLineData = self.MakeIndividualLineData(individualLine,recipeData,buildingData)
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
        filePath = pathData.GetPath() + "\\" + self.INDIVIDUAL_LINE_DIRECTORY_NAME
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
        individualLine = IndividualLineEssenceModule.IndividualLineEssence(jsonData)
        return individualLine


    # レシピデータを読み込み
    def ReadRecipeFile(self,individualLine):
        recipes = recipeManagerModule.RecipeReader()
        recipe = recipes.GetRecipe(individualLine.GetRecipeName())
        return recipe
    
    # 設備データを読み込み
    def ReadBuildingInfoFile(self,recipe:recipeManagerModule.RecipeItem) -> BuildingDataManagerModule.BuildingDataItem:
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
    def MakeIndividualLineData(self,individualLine,recipeData,buildingData):
        replaceData = IndividualLineDataModule.IndividualLineData()

        # ライン名を追加
        replaceData.Append(replaceData.LINE_NAME_KEY,individualLine.GetLineName())

        # レシピ名を追加
        replaceData.Append(replaceData.RECIPE_NAME_KEY,recipeData.GetRecipeName())
        recipeNum = individualLine.GetRecipeNum()
        replaceData.Append(replaceData.RECIPE_NUM_KEY,recipeNum)

        # 制作物を追加
        productName = recipeData.GetProductName()
        replaceData.Append(replaceData.PRODUCT_NAME_KEY,productName)

        # 合計コストを追加
        buildingReader = BuildingDataManagerModule.BuildingDataReader()
        buildingData = buildingReader.GetBuildingData(productName)
        costList = []
        for cost in buildingData.GetCostList():
            costList.append({
                replaceData.ITEM_NAME_KEY : cost[buildingData.ITEM_NAME_KEY],
                replaceData.ITEM_NUM_KEY : cost[buildingData.ITEM_NUM_KEY] * recipeNum

            })
        replaceData.Append(replaceData.COST_LIST_KEY,costList)

        # 合計消費電力を追加
        totalUsePower = buildingData.GetUsePower() * recipeNum
        replaceData.Append(replaceData.TOTAL_USE_POWER_KEY,totalUsePower)

        # 搬入物を追加
        index = 0
        for data in recipeData.GetInputItemList():
            inputNameKey = replaceData.INPUT_NAME_KEY + str(index+1)
            inputName = data[recipeData.ITEM_NAME_KEY]
            replaceData.Append(inputNameKey, inputName)
            
            inputNumKey = replaceData.INPUT_NUM_KEY + str(index+1)
            inputNum = data[recipeData.ITEM_NUM_KEY]
            replaceData.Append(inputNumKey ,inputNum)
            
            inputTotalKey = replaceData.TOTAL_INPUT_KEY + str(index+1)
            inputTotal = recipeNum*inputNum
            replaceData.Append(inputTotalKey,inputTotal)
            
            index = index + 1
        
        # 搬出物を追加
        index = 0
        for data in recipeData.GetOutputItemList():
            outputNameKey = replaceData.OUTPUT_NAME_KEY + str(index+1)
            outputName = data[recipeData.ITEM_NAME_KEY]
            replaceData.Append(outputNameKey, outputName)
            
            outputNumKey = replaceData.OUTPUT_NUM_KEY + str(index+1)
            outputNum = data[recipeData.ITEM_NUM_KEY]
            replaceData.Append(outputNumKey ,outputNum)
            
            outputTotalKey = replaceData.TOTAL_OUTPUT_KEY + str(index+1)
            outputTotal = recipeNum*outputNum
            replaceData.Append(outputTotalKey,outputTotal)

            index = index + 1

                    
        return replaceData


    # 置き換え
    def Replace(self,text,replaceData):
        for key in replaceData.GetKeys():
            text = text.replace(replaceData.GetReplaceKey(key),str(replaceData.value[key]))
        return text
    
    
    # 複数の Input 物品を記載するため、行を複製
    def DuplicateInputItem(self,templateLines,recipeData,replaceData):
        resultLines = []
        inputLength = int(recipeData.GetInputItemLength())

        inputNameKey = replaceData.INPUT_NAME_KEY
        inputReplaceNameKey = replaceData.GetReplaceKey(inputNameKey)
        
        inputNumKey = replaceData.INPUT_NUM_KEY
        inputReplaceNumKey = replaceData.GetReplaceKey(inputNumKey)

        inputTotalKey = replaceData.TOTAL_INPUT_KEY
        inputReplaceTotalKey = replaceData.GetReplaceKey(inputTotalKey)
        
        for i in range(len(templateLines)):
            if not(replaceData.INPUT_NAME_KEY in templateLines[i]):
                resultLines.append(templateLines[i])
                continue
            
            for f in range(inputLength):
                line = templateLines[i].replace(inputReplaceNameKey, inputReplaceNameKey + str(f+1))
                line = line.replace(inputReplaceNumKey, inputReplaceNumKey + str(f+1))
                line = line.replace(inputReplaceTotalKey, inputReplaceTotalKey + str(f+1))
                resultLines.append(line)

        return resultLines
        
    
    # 複数の Output 物品を記載するため、行を複製
    def DuplicateOutputItem(self,templateLines,recipeData,replaceData):
        resultLines = []
        outputLength = int(recipeData.GetOutputItemLength())

        outputNameKey = replaceData.OUTPUT_NAME_KEY
        outputReplaceNameKey = replaceData.GetReplaceKey(outputNameKey)
        
        outputNumKey = replaceData.OUTPUT_NUM_KEY
        outputReplaceNumKey = replaceData.GetReplaceKey(outputNumKey)

        outputTotalKey = replaceData.TOTAL_OUTPUT_KEY
        outputReplaceTotalKey = replaceData.GetReplaceKey(outputTotalKey)
        
        for i in range(len(templateLines)):
            if not(replaceData.OUTPUT_NAME_KEY in templateLines[i]):
                resultLines.append(templateLines[i])
                continue
            
            for f in range(outputLength):
                line = templateLines[i].replace(outputReplaceNameKey, outputReplaceNameKey + str(f+1))
                line = line.replace(outputReplaceNumKey, outputReplaceNumKey + str(f+1))
                line = line.replace(outputReplaceTotalKey, outputReplaceTotalKey + str(f+1))
                resultLines.append(line)

        return resultLines


    def MakeFlowChart(self,replaceData):

        result = []
        inputName = replaceData.GetReplaceKey(replaceData.INPUT_NAME_KEY)
        inputNum = replaceData.GetReplaceKey(replaceData.INPUT_NUM_KEY)
        outputName = replaceData.GetReplaceKey(replaceData.OUTPUT_NAME_KEY)
        outputNum = replaceData.GetReplaceKey(replaceData.OUTPUT_NUM_KEY)
        productName = replaceData.GetReplaceKey(replaceData.PRODUCT_NAME_KEY)
        productNum = replaceData.GetRecipeNum()
            
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


