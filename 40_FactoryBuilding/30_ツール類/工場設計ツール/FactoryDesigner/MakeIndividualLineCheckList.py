import os
import json

from DesignModules import InfomationReaderModule as RecipeReader
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
        iLineData = self.MakeReplaceData(iLineEssence)


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
            iLineEssence :ILineEssence.IndividualLineEssence
            ):
        

        iLineData = ILineData.IndividualLineData(iLineEssence)

        return iLineData


    # 置き換え
    def Replace(
            self,
            text : str,
            iLineData : ILineData.IndividualLineData):
        for key in iLineData.GetKeys():
            text = text.replace(iLineData.GetReplaceKey(key),str(iLineData.GetValue(key)))
        return text
    

    # 複数の Product を記載するため、行を複製
    def DuplicateProductItem(
            self,
            templateLines,
            iLineEssence : ILineEssence.IndividualLineEssence,
            iLineData : ILineData.IndividualLineData
            ):


        resultLines = []
        productLength = int(iLineEssence.GetValue(ILineEssence.RECIPE_NUM_KEY))

        productNameKey = ILineData.PRODUCT_NAME_KEY
        productReplaceNameKey = iLineData.GetReplaceKey(productNameKey)
        
        for i in range(len(templateLines)):
            if not(ILineData.PRODUCT_NAME_KEY in templateLines[i]):
                resultLines.append(templateLines[i])
                continue
            
            for f in range(productLength):
                line = templateLines[i].replace(productReplaceNameKey, productReplaceNameKey + str(f+1))
                resultLines.append(line)
                
        return resultLines


    # 複数の Input 物品を記載するため、行を複製
    def DuplicateInputItem(
            self,
            templateLines,
            recipeItem : RecipeItem.RecipeItem,
            iLineData : ILineData.IndividualLineData):
        
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
            iLineData : ILineData.IndividualLineData):
        
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


