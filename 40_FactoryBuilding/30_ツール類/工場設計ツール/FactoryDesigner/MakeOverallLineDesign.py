import os
import json

from DesignModules import recipeManagerModule
from DesignModules import BuildingDataManagerModule
from DesignModules import OverallLineDataModule
from DesignModules import OverallLineEssenceModule
from DesignModules import IndividualLineEssenceModule
from DesignModules import pathDataModule

# 全体製造ライン設計書作成用クラス
class OverallLineDesignMaker:

    # constans
    TEMPLATE_FILE_NAME = './全体製造ライン設計書_var_factoryName.md'
    OVERALL_LINE_ESSENCE_NAME = './OverallLineESSENCE.json'
    OVERALL_LINE_DATA_NAME = './OverallLineData.json'
    OUTPUT_FILE_NAME = '全体製造ライン設計書_var_factoryName.md'

    FACTORY_NAME_KEY_WORD = "var_factoryName"
    RECIPIES_KEY_WORD = "var_recipies"
    LINES_KEY_WORD = "var_lines"
    FLOWCHART_KEY_WORD = "var_flowChart"

    # クラス変数

    # 全体ラインデータ
    overallLineEssence = 0
    overallLineData = 0
    
    # 個別ライン本質リスト
    individualLineEssences = 0
    

    def Main(self,pathData : pathDataModule.PathData) -> OverallLineDataModule.OverallLineData:

        # ファイルのフルパスを取得
        inputDataFileName = pathData.GetFullPath()
        if inputDataFileName == "":
            inputDataFileName = self.inputDataFileName


        # 全体ライン本質を読み込み
        overallLineEssence = self.ReadOverallLineEssence(inputDataFileName)
        self.overallLineEssence = overallLineEssence

        # 全体ラインデータを作成
        overallLineData = self.MakeOLineData(overallLineEssence)
        overallLineData.Output(pathData.GetPath())

        # 個別ライン本質リストの作成
        self.individualLineEssences = self.MakeILineEssence(overallLineData)

        # 全体ラインテンプレートを読み込み
        templateLines = self.ReadTemplateFile()
        
        # 置換用データを作成
        recipeText = self.MakeRecipesText(overallLineData)
        linesText = self.MakeIndividualLinesText(overallLineData)
        flowchartText = self.MakeFlowChart(overallLineData)

        # 置き換え
        result = []
        for line in templateLines :
            text = line
            text = text.replace(self.RECIPIES_KEY_WORD,recipeText)
            text = text.replace(self.LINES_KEY_WORD,linesText)
            text = text.replace(self.FLOWCHART_KEY_WORD,flowchartText)
            text = text.replace(self.FACTORY_NAME_KEY_WORD,overallLineData.GetValue(overallLineData.FACTORY_NAME_KEY))
            result.append(text)

        # print(result)

        # text output
        filePath = pathData.GetPath()
        fileName = self.OUTPUT_FILE_NAME.replace(self.FACTORY_NAME_KEY_WORD,overallLineData.GetValue(overallLineData.FACTORY_NAME_KEY))
        self.WriteFile(filePath,fileName,result)

        return overallLineData


    # テンプレートファイルを読み込み
    def ReadTemplateFile(self) -> list:
        lines = []
        os.chdir(os.path.dirname(__file__) + "/../")
        with open(self.TEMPLATE_FILE_NAME, encoding="utf-8") as f:
            for line in f:
                lines.append(line.rstrip())
        return lines
    

    # 全体ライン本質ファイルを読み込み
    def ReadOverallLineEssence(self,overallLineEssenceName) -> OverallLineEssenceModule.OverallLineEssence:
        jsonData = json.load(open(overallLineEssenceName,'r', encoding="utf-8"))
        overallLine = OverallLineEssenceModule.OverallLineEssence(jsonData)
        return overallLine


    # 全体ラインデータファイルを読み込み
    def ReadOverallLineData(self,overallLineDataName) -> OverallLineDataModule.OverallLineData:
        jsonData = json.load(open(overallLineDataName,'r', encoding="utf-8"))
        overallLine = OverallLineDataModule.OverallLineData(jsonData)
        return overallLine
    
    # 全体ラインデータファイルの作成
    def MakeOLineData(self,oLineEssence :OverallLineEssenceModule.OverallLineEssence) -> OverallLineDataModule.OverallLineData:

        oLineDefine = OverallLineDataModule.OverallLineData([])

        # 返す用データを作成
        result = {}

        # 工場名
        result[oLineDefine.FACTORY_NAME_KEY] = oLineEssence.GetValue(oLineEssence.FACTORY_NAME_KEY)


        # 使用レシピ
        recipeList = []
        for useRecipe in oLineEssence.GetValue(oLineEssence.RECIPE_LIST_KEY):

            recipeData = self.ReadRecipeFile(useRecipe[oLineEssence.RECIPE_NAME_KEY])
            
            recipeDict = {}

            # レシピ名
            recipeDict[oLineDefine.RECIPE_NAME_KEY] = recipeData.GetRecipeName()

            # 要求物品
            inputList = []
            for recipeItemData in recipeData.GetInputItemList():
                overallItemData = {}
                overallItemData[oLineDefine.ITEM_NAME_KEY] = recipeItemData[recipeData.ITEM_NAME_KEY]
                overallItemData[oLineDefine.ITEM_NUM_KEY] = recipeItemData[recipeData.ITEM_NUM_KEY]
                inputList.append(overallItemData)
            recipeDict[oLineDefine.INPUT_LIST_KEY] = inputList

            # 加工物品
            outputList = []
            for recipeItemData in recipeData.GetOutputItemList():
                overallItemData = {}
                overallItemData[oLineDefine.ITEM_NAME_KEY] = recipeItemData[recipeData.ITEM_NAME_KEY]
                overallItemData[oLineDefine.ITEM_NUM_KEY] = recipeItemData[recipeData.ITEM_NUM_KEY]
                outputList.append(overallItemData)
            recipeDict[oLineDefine.OUTPUT_LIST_KEY] = outputList

            recipeList.append(recipeDict)

        result[oLineDefine.RECIPE_LIST_KEY] = recipeList


        # 個別ラインリスト
        iLineList = []
        for useRecipe in oLineEssence.GetValue(oLineEssence.RECIPE_LIST_KEY):

            recipeData = self.ReadRecipeFile(useRecipe[oLineEssence.RECIPE_NAME_KEY])

            iLineDict = {}

            # 製造ライン名
            iLineDict[oLineDefine.INDIVIDUAL_LINE_NAME] = recipeData.GetRecipeName() + "製造ライン"

            # レシピ名
            iLineDict[oLineDefine.RECIPE_NAME_KEY] = recipeData.GetRecipeName()
          
            # レシピ数
            recipeNum = useRecipe[oLineEssence.RECIPE_NUM_KEY]
            iLineDict[oLineDefine.RECIPE_NUM_KEY] = recipeNum

            # 要求物品
            inputList = []
            for recipeItemData in recipeData.GetInputItemList():
                overallItemData = {}
                overallItemData[oLineDefine.ITEM_NAME_KEY] = recipeItemData[recipeData.ITEM_NAME_KEY]
                overallItemData[oLineDefine.ITEM_NUM_KEY] = recipeItemData[recipeData.ITEM_NUM_KEY] * recipeNum
                inputList.append(overallItemData)
            iLineDict[oLineDefine.INPUT_LIST_KEY] = inputList

            # 加工物品
            outputList = []
            for recipeItemData in recipeData.GetOutputItemList():
                overallItemData = {}
                overallItemData[oLineDefine.ITEM_NAME_KEY] = recipeItemData[recipeData.ITEM_NAME_KEY]
                overallItemData[oLineDefine.ITEM_NUM_KEY] = recipeItemData[recipeData.ITEM_NUM_KEY] * recipeNum
                outputList.append(overallItemData)
            iLineDict[oLineDefine.OUTPUT_LIST_KEY] = outputList

            iLineList.append(iLineDict)

        result[oLineDefine.INDIVIDUAL_LINE_LIST] = iLineList


        # 入力ライン
        result[oLineDefine.INPUT_LINE_LIST] = oLineEssence.GetValue(oLineEssence.INPUT_LINE_LIST)
        
        # 出力ライン
        result[oLineDefine.OUTPUT_LINE_LIST] = oLineEssence.GetValue(oLineEssence.OUTPUT_LINE_LIST)
        
        # 製造ライン関係性
        result[oLineDefine.RELATIONSHIPS_KEY] = oLineEssence.GetValue(oLineEssence.RELATIONSHIPS_KEY)

        return OverallLineDataModule.OverallLineData(result)

    # 個別ライン本質ファイルの作成
    def MakeILineEssence(self,oLineData :OverallLineDataModule.OverallLineData) -> list:
        result = []

        # 個別ラインの情報を取得
        iLines = oLineData.GetValue(oLineData.INDIVIDUAL_LINE_LIST)

        # 個別ラインの情報から、個別ライン本質を作成し、リストへ加える
        iLineDefine = IndividualLineEssenceModule.IndividualLineEssence([])
        for iLine in iLines:
            lineEssense = {}
            lineEssense[iLineDefine.LINE_NAME_KEY] = iLine[oLineData.INDIVIDUAL_LINE_NAME]
            lineEssense[iLineDefine.RECIPE_NAME_KEY] = iLine[oLineData.RECIPE_NAME_KEY]
            lineEssense[iLineDefine.RECIPE_NUM_KEY] = iLine[oLineData.RECIPE_NUM_KEY]
            result.append(IndividualLineEssenceModule.IndividualLineEssence(lineEssense))

        return result


    # レシピデータを読み込み
    def ReadRecipeFile(self,recipeName:str) -> recipeManagerModule.RecipeItem:
        recipes = recipeManagerModule.RecipeReader()
        recipe = recipes.GetRecipe(recipeName)
        return recipe
    

    # 設備データを読み込み
    def ReadBuildingDataFile(self,recipe:recipeManagerModule.RecipeItem) -> BuildingDataManagerModule.BuildingDataItem:
        buildingInfo = BuildingDataManagerModule.BuildingDataReader()
        buildingInfo = BuildingDataManagerModule.BuildingDataReader.GetBuildingInfo(recipe.GetProductName())
        return buildingInfo
    
    
    # 保存
    def WriteFile(self,filePath,fileName,lines):
        os.chdir(os.path.dirname(__file__) + "/../")
        os.chdir(filePath)
        with open(fileName,"w", encoding="utf-8") as o:
            for line in lines:
                print(line,file=o)
        return
    

    # レシピ群の置き換え用の文字列を返す
    def MakeRecipesText(self,overallData:OverallLineDataModule.OverallLineData) -> list:
        
        # 返す用変数を作成
        result = ""

        # レシピリストの取得 
        recipeList = overallData.GetValue(overallData.RECIPE_LIST_KEY)

        # レシピごとの文章を加算
        for recipe in recipeList:
            result += self.MakeRecipeText(recipe[overallData.RECIPE_NAME_KEY])
        
        return result
    

    # レシピ単体の置き換え用文字列を返す
    def MakeRecipeText(self,recipeName:str) -> str:
        
        # レシピデータ取得
        recipe = self.ReadRecipeFile(recipeName)

        # ヘッダー
        result = "### " + recipe.GetRecipeName() + "\n"
        result += "|I/O|物品名|要求数|\n"
        result += "|---|---|---|\n"

        
        # input 
        items = recipe.GetInputItemList()
        for item in items:
            result += "|input|" + str(item[recipe.ITEM_NAME_KEY]) + "|" + str(item[recipe.ITEM_NUM_KEY]) + "|\n"

        result += "|---|---|---|\n"

        # input 
        items = recipe.GetOutputItemList()
        for item in items:
            result += "|output|" + str(item[recipe.ITEM_NAME_KEY]) + "|" + str(item[recipe.ITEM_NUM_KEY]) + "|\n"

        return result
    

    # 個別ラインリストの置き換え用の文字列を返す
    def MakeIndividualLinesText(self,overallData:OverallLineDataModule.OverallLineData) -> list:
        
        # 返す用変数を作成
        result = ""

        # 個別ラインリストの取得 
        lineList = overallData.GetValue(overallData.INDIVIDUAL_LINE_LIST)

        # 個別ラインごとの文章を加算
        for line in lineList:
            result += self.MakeIndividualLineText(line)
        
        return result
    

    # 個別ライン単体の置き換え用文字列を返す
    def MakeIndividualLineText(self,iLineData:dict) -> str:
        
        overall = OverallLineDataModule.OverallLineData([])

        # タイトル
        result = "### " + iLineData[overall.INDIVIDUAL_LINE_NAME] + "\n"
        result += "\n"
        
        # 基本情報
        result += "レシピ名 : " + iLineData[overall.RECIPE_NAME_KEY] + "  \n"
        result += "レシピ数 : " + str(iLineData[overall.RECIPE_NUM_KEY]) + "\n"
        result += "\n"
        
        # ヘッダー
        result += "|I/O|物品名|要求数|\n"
        result += "|---|---|---|\n"

        
        # input 
        items = iLineData[overall.INPUT_LIST_KEY]
        for item in items:
            result += "|input|" + str(item[overall.ITEM_NAME_KEY]) + "|" + str(item[overall.ITEM_NUM_KEY]) + "|\n"

        result += "|---|---|---|\n"

        # output 
        items = iLineData[overall.OUTPUT_LIST_KEY]
        for item in items:
            result += "|output|" + str(item[overall.ITEM_NAME_KEY]) + "|" + str(item[overall.ITEM_NUM_KEY]) + "|\n"

        result += "\n"
        result += "\n"

        return result


    # フローチャート作成
    def MakeFlowChart(self,overallData:OverallLineDataModule.OverallLineData) -> str:

        result = ""
        inputList = overallData.GetValue(overallData.INPUT_LINE_LIST)
        lineList = overallData.GetValue(overallData.INDIVIDUAL_LINE_LIST)
        outputList = overallData.GetValue(overallData.OUTPUT_LINE_LIST)
        relationships = overallData.GetValue(overallData.RELATIONSHIPS_KEY)
            
        # header
        result = "```mermaid\n"
        result += "flowchart TD\n"


        # input
        result += "subgraph Input\n"
        for inputName in inputList:
            result += "    " + inputName +"([" + inputName + "])\n"
        result += "end\n\n"

        # product
        for line in lineList:
            result += line[overallData.INDIVIDUAL_LINE_NAME] + "\n"
        result += "\n"

        # output
        result += "subgraph Output\n"
        for outputName in outputList:
            result += "    " + outputName +"([" + outputName + "])\n"
        result += "end\n\n"


        # flow
        for relation in relationships:
            supplierLine = relation[overallData.SUPPLYER_LINE_KEY]
            destinationLine = relation[overallData.DESTINATION_LINE_KEY]
            supplyItem = relation[overallData.SUPPLY_ITEM_KEY]
            supplyNum = relation[overallData.SUPPLY_NUM_KEY]
            result += supplierLine + "-->|" + supplyItem + str(supplyNum) + "|" + destinationLine + "\n"

        result += "```\n"
        
        return result


