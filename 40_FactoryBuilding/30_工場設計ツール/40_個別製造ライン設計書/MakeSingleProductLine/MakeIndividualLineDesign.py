import os
import json

from MakeIndividualLineDesignModules import recipeManagerModule
from MakeIndividualLineDesignModules import individualLineDataModule
from MakeIndividualLineDesignModules import replaceDataModule


class IndividualLineDesignMaker:

    # constans
    inputTextFileName = './個別製造ライン設計書_var_outputName製造ライン.md'
    inputDataFileName = './IndividualLine.json'
    outputFileName = '個別製造ライン設計書_var_outputName製造ライン.md'
    


    inputNum = 0
    outputNum = 0


    def Main(self,argv):

        inputDataFileName = self.inputDataFileName
        if len(argv) != 1:
            if argv[1] != "":
                inputDataFileName = argv[1]

        # input file read
        templateLines = self.ReadTemplateFile()
        individualLine = self.ReadIndividualLineFile(inputDataFileName)
        recipeData = self.ReadRecipeFile(individualLine)

        # 置換用データを作成
        replaceData = self.MakeReplaceData(individualLine,recipeData)

        # MakeFlowChart
        insertNum = 0
        for index, item in enumerate(templateLines):
            if item == "## 製造ライン":
                insertNum = index + 1
                break

        flowChart = self.MakeFlowChart(replaceData)

        for chartLine in flowChart:
            templateLines.insert(insertNum,chartLine)
            insertNum += 1


        # replace
        for index, item in enumerate(templateLines):
            templateLines[index] = self.Replace(templateLines[index],replaceData)


        # text output
        filePath = "./"
        if len(argv) != 1:
            filePath = argv[2]
        fileName = self.Replace(self.outputFileName,replaceData)
        self.WriteFile(filePath,fileName,templateLines)


    # テンプレートファイルを読み込み
    def ReadTemplateFile(self):
        lines = []
        os.chdir(os.path.dirname(__file__) + "/../")
        with open(self.inputTextFileName, encoding="utf-8") as f:
            for line in f:
                lines.append(line.rstrip())
        return lines


    # 個別ラインデータを読み込み
    def ReadIndividualLineFile(self,inputDataFileName):
        jsonData = json.load(open(inputDataFileName,'r', encoding="utf-8"))
        individualLine = individualLineDataModule.IndividualLineData(jsonData)
        return individualLine


    # レシピデータを読み込み
    def ReadRecipeFile(self,individualLine):
        recipes = recipeManagerModule.RecipeReader()
        recipe = recipes.GetRecipe(individualLine.GetRecipeName())
        return recipe
    

    # 保存
    def WriteFile(self,filePath,fileName,lines):
        os.chdir(os.path.dirname(__file__) + "/../")
        os.chdir(filePath)
        with open(fileName,"w", encoding="utf-8") as o:
            for line in lines:
                print(line,file=o)
        return


    # 置き換え用データを作成
    def MakeReplaceData(self,individualLine,recipeData):
        replaceData = replaceDataModule.ReplaceData()

        # レシピ名を追加
        replaceData.Append(replaceData.RECIPE_NAME_KEY,recipeData.GetRecipeName())
        recipeNum = individualLine.GetRecipeNum()
        replaceData.Append(replaceData.RECIPE_NUM_KEY,recipeNum)

        # 制作物を追加
        replaceData.Append(replaceData.PRODUCT_NAME_KEY,recipeData.GetProductName())

        # 搬入物を追加
        inputData = recipeData.GetInputItemList()[0]
        replaceData.Append(replaceData.INPUT_NAME_KEY,inputData[recipeData.ITEM_NAME_KEY])
        inputNum = inputData[recipeData.ITEM_NUM_KEY]
        replaceData.Append(replaceData.INPUT_NUM_KEY,inputNum)
        
        # 搬出物を追加
        outputData = recipeData.GetOutputItemList()[0]
        replaceData.Append(replaceData.OUTPUT_NAME_KEY,outputData[recipeData.ITEM_NAME_KEY])
        outputNum = outputData[recipeData.ITEM_NUM_KEY]
        replaceData.Append(replaceData.OUTPUT_NUM_KEY,outputNum)
        
        # 合計入出力
        replaceData.Append(replaceData.TOTAL_INPUT_KEY,str(recipeNum*inputNum))
        replaceData.Append(replaceData.TOTAL_OUTPUT_KEY,str(recipeNum*outputNum))
        return replaceData


    # 置き換え
    def Replace(self,text,replaceData):
        for key in replaceData.GetKeys():
            text = text.replace("var_" + key,str(replaceData.value[key]))
        return text


    def MakeFlowChart(self,replaceData):

        result = []
        inputName = replaceData.GetInputName()
        inputNum = replaceData.GetInputNum()
        outputName = replaceData.GetOutputName()
        outputNum = replaceData.GetOutputNum()
        productName = replaceData.GetProductName()
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


