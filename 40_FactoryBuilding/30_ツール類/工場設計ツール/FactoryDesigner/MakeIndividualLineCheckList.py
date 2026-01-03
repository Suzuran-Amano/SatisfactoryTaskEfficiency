import os
import json

from DesignModules import RecipeReaderModule as RecipeReader
from DesignModules import RecipeItemModule as RecipeItem
from DesignModules import IndividualLineEssenceModule as ILineEssence
from DesignModules import IndividualLineDataModule as ILineData
from DesignModules import pathDataModule


# 個別製造ラインテスト項目書作成
class MakeIndividualLineCheckList:

    # constans
    inputTextFileName = './個別製造ラインテスト項目書_var_lineName.md'
    inputDataFileName = './IndividualLine.json'
    outputFileName = '個別製造ラインテスト項目書_var_lineName.md'
    



    inputNum = 0
    outputNum = 0


    def Main(self,
            pathData : pathDataModule.PathData,
            iLineEssence : ILineEssence.IndividualLineEssence
            ):

        # input file read
        templateLines = self.ReadTemplateFile()
        recipeData = RecipeReader.GetRecipe(iLineEssence.GetValue(ILineEssence.RECIPE_NAME_KEY))

        # 置換用データを作成
        iLineData = self.MakeReplaceData(iLineEssence,recipeData)


        # replace
        templateLines = self.DuplicateProductItem(templateLines,iLineEssence,iLineData)
        templateLines = self.DuplicateInputItem(templateLines,recipeData,iLineData)
        templateLines = self.DuplicateOutputItem(templateLines,recipeData,iLineData)
        for index, item in enumerate(templateLines):
            templateLines[index] = self.Replace(templateLines[index],iLineData)


        # text output
        filePath = pathData.GetPath() + pathDataModule.INDIVIDUAL_TEST_DIRECTORY_NAME
        fileName = self.Replace(self.outputFileName,iLineData)
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
        iLineEssence = ILineEssence.IndividualLineEssence(jsonData)
        return iLineEssence


    # 保存
    def WriteFile(self,filePath,fileName,lines):
        os.makedirs(filePath, exist_ok=True)
        os.chdir(os.path.dirname(__file__) + "/../")
        os.chdir(filePath)
        with open(fileName,"w", encoding="utf-8") as o:
            for line in lines:
                print(line,file=o)
        return


    # 置き換え用データを作成
    def MakeReplaceData(self,
            iLineEssence :ILineEssence.IndividualLineEssence,
            recipeData):
        

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
        iLineData.Append(iLineData.PRODUCT_NAME_KEY,recipeData.GetProductName())

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
            inputTotal = str(recipeNum*inputNum)
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
            outputTotal = str(recipeNum*outputNum)
            iLineData.Append(outputTotalKey,outputTotal)

            index = index + 1
                    
        return iLineData


    # 置き換え
    def Replace(self,text,iLineData):
        for key in iLineData.GetKeys():
            text = text.replace(iLineData.GetReplaceKey(key),str(iLineData.value[key]))
        return text
    

    # 複数の Product を記載するため、行を複製
    def DuplicateProductItem(
            self,
            templateLines,
            iLineEssence : ILineEssence.IndividualLineEssence,
            iLineData):


        resultLines = []
        productLength = int(iLineEssence.GetValue(ILineEssence.RECIPE_NUM_KEY))

        productNameKey = iLineData.PRODUCT_NAME_KEY
        productReplaceNameKey = iLineData.GetReplaceKey(productNameKey)
        
        for i in range(len(templateLines)):
            if not(iLineData.PRODUCT_NAME_KEY in templateLines[i]):
                resultLines.append(templateLines[i])
                continue
            
            for f in range(productLength):
                line = templateLines[i].replace(productReplaceNameKey, productReplaceNameKey + str(f+1))
                resultLines.append(line)
                
        return resultLines


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


