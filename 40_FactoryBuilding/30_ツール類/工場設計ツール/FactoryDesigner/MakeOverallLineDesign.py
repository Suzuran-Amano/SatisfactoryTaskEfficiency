import os
import json

from DesignModules import recipeManagerModule
from DesignModules import BuildingDataManagerModule
from DesignModules import IndividualLineEssenceModule
from DesignModules import OverallLineDataModule
from DesignModules import pathDataModule

# 全体製造ライン設計書作成用クラス
class OverallLineDesignMaker:

    # constans
    TEMPLATE_FILE_NAME = './全体製造ライン設計書_var_factoryName.md'
    OVERALL_LINE_DATA_NAME = './OverallLineData.json'
    OUTPUT_FILE_NAME = '全体製造ライン設計書_var_factoryName.md'

    FACTORY_NAME_KEY_WORD = "var_factoryName"
    RECIPIES_KEY_WORD = "var_recipies"
    LINES_KEY_WORD = "var_lines"
    FLOWCHART_KEY_WORD = "var_flowChart"

    # クラス変数

    # 全体ラインデータ
    overallLineData = 0
    
    # 個別ライン本質リスト
    individualLineEssences = 0
    

    def Main(self,pathData : pathDataModule.PathData):

        # ファイルのフルパスを取得
        inputDataFileName = pathData.GetFullPath()
        if inputDataFileName == "":
            inputDataFileName = self.inputDataFileName

        # 全体ラインデータを読み込み
        overallLineData = self.ReadOverallLineData(self.OVERALL_LINE_DATA_NAME)
        self.overallLineData = overallLineData

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

        return


    # テンプレートファイルを読み込み
    def ReadTemplateFile(self) -> list:
        lines = []
        os.chdir(os.path.dirname(__file__) + "/../")
        with open(self.TEMPLATE_FILE_NAME, encoding="utf-8") as f:
            for line in f:
                lines.append(line.rstrip())
        return lines


    # 全体ラインデータファイルを読み込み
    def ReadOverallLineData(self,overallLineDataName) -> OverallLineDataModule.OverallLineData:
        jsonData = json.load(open(overallLineDataName,'r', encoding="utf-8"))
        overallLine = OverallLineDataModule.OverallLineData(jsonData)
        return overallLine
    

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


