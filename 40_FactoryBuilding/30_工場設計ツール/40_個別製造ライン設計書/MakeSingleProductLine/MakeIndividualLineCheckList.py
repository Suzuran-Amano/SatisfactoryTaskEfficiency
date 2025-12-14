import os
import json

from MakeIndividualLineDesignModules import recipeManagerModule
from MakeIndividualLineDesignModules import individualLineDataModule
from MakeIndividualLineDesignModules import replaceDataModule
from MakeIndividualLineDesignModules import pathDataModule

# 個別製造ラインテスト項目書作成
class MakeIndividualLineCheckList:

    # constans
    inputTextFileName = './個別製造ラインテスト項目書_var_recipeName製造ライン.md'
    inputDataFileName = './IndividualLine.json'
    outputFileName = '個別製造ラインテスト項目書_var_recipeName製造ライン.md'
    


    inputNum = 0
    outputNum = 0


    def Main(self,pathData : pathDataModule.PathData):

        # ファイルのフルパスを取得
        inputDataFileName = pathData.GetFullPath()
        if inputDataFileName == "":
            inputDataFileName = self.inputDataFileName

        # input file read
        templateLines = self.ReadTemplateFile()
        individualLine = self.ReadIndividualLineFile(inputDataFileName)
        recipeData = self.ReadRecipeFile(individualLine)

        # 置換用データを作成
        replaceData = self.MakeReplaceData(individualLine,recipeData)


        # replace
        templateLines = self.DuplicateProductItem(templateLines,individualLine,replaceData)
        templateLines = self.DuplicateInputItem(templateLines,recipeData,replaceData)
        templateLines = self.DuplicateOutputItem(templateLines,recipeData,replaceData)
        for index, item in enumerate(templateLines):
            templateLines[index] = self.Replace(templateLines[index],replaceData)


        # text output
        filePath = pathData.GetPath()
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
        index = 0
        for data in recipeData.GetInputItemList():
            inputNameKey = replaceData.INPUT_NAME_KEY + str(index+1)
            inputName = data[recipeData.ITEM_NAME_KEY]
            replaceData.Append(inputNameKey, inputName)
            
            inputNumKey = replaceData.INPUT_NUM_KEY + str(index+1)
            inputNum = data[recipeData.ITEM_NUM_KEY]
            replaceData.Append(inputNumKey ,inputNum)
            
            inputTotalKey = replaceData.TOTAL_INPUT_KEY + str(index+1)
            inputTotal = str(recipeNum*inputNum)
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
            outputTotal = str(recipeNum*outputNum)
            replaceData.Append(outputTotalKey,outputTotal)

            index = index + 1
                    
        return replaceData


    # 置き換え
    def Replace(self,text,replaceData):
        for key in replaceData.GetKeys():
            text = text.replace(replaceData.GetReplaceKey(key),str(replaceData.value[key]))
        return text
    

    # 複数の Product を記載するため、行を複製
    def DuplicateProductItem(self,templateLines,individualLine,replaceData):
        resultLines = []
        productLength = int(individualLine.GetRecipeNum())

        productNameKey = replaceData.PRODUCT_NAME_KEY
        productReplaceNameKey = replaceData.GetReplaceKey(productNameKey)
        
        for i in range(len(templateLines)):
            if not(replaceData.PRODUCT_NAME_KEY in templateLines[i]):
                resultLines.append(templateLines[i])
                continue
            
            for f in range(productLength):
                line = templateLines[i].replace(productReplaceNameKey, productReplaceNameKey + str(f+1))
                resultLines.append(line)
                
        return resultLines


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


