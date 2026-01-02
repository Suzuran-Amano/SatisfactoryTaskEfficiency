import os
import json

from DesignModules import recipeManagerModule
from DesignModules import BuildingDataManagerModule
from DesignModules import OverallLineEssenceModule
from DesignModules import OverallLineDataModule
from DesignModules.OverallLineDocumentModule import OverallLineDocument as OLineDoc
from DesignModules import IndividualLineEssenceModule
from DesignModules import pathDataModule

# 全体製造ライン設計書作成用クラス
class OverallLineDesignMaker:

    # constans
    OVERALL_LINE_DIRECTORY_NAME = "30_全体製造ライン設計書"
    INDIVIDUAL_LINE_DIRECTORY_NAME = "40_個別製造ライン設計書"

    OVERALL_LINE_ESSENCE_NAME = './OverallLineEssence.json'

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

        # 全体ライン書類を出力
        iverallLineDocument = OLineDoc()
        iverallLineDocument.OutputDocument(pathData,overallLineData)

        # 個別ライン本質リストの作成
        individualLineEssences = self.MakeILineEssence(overallLineData)
        self.individualLineEssences = individualLineEssences
        for iLineEssence in individualLineEssences :
            iLineEssence.Output(pathData.GetPath())


        return overallLineData
    

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
    
    