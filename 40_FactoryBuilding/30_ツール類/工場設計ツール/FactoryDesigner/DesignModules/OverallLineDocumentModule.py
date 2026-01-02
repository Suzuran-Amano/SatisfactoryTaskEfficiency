import os

from .OverallLineDataModule import OverallLineData as OLineData
from . import  pathDataModule
from .pathDataModule import  PathData
from .recipeManagerModule import RecipeItem
from .recipeManagerModule import RecipeReader


# 全体ライン設計書を管理するクラス
class OverallLineDocument():

    # 定数
    TEMPLATE_FILE_NAME = './全体製造ライン設計書_var_factoryName.md'
    OUTPUT_FILE_NAME = '全体製造ライン設計書_var_factoryName.md'

    FACTORY_NAME_KEY_WORD = "var_factoryName"
    RECIPIES_KEY_WORD = "var_recipies"
    LINES_KEY_WORD = "var_lines"
    FLOWCHART_KEY_WORD = "var_flowChart"


    def __init__(self):
    
        return
    

    # 全体ライン書類を保存
    def OutputDocument(
            self,
            pathData : PathData,
            overallLineData : OLineData):


        # 全体ラインテンプレートを読み込み
        templateLines = self._ReadTemplateFile()

        # 置換用データを作成
        recipeText = self._MakeRecipesText(overallLineData)
        linesText = self._MakeIndividualLinesText(overallLineData)
        flowchartText = self._MakeFlowChart(overallLineData)

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
        filePath = pathData.GetPath() + "\\" + pathDataModule.OVERALL_LINE_DIRECTORY_NAME
        fileName = self.OUTPUT_FILE_NAME.replace(self.FACTORY_NAME_KEY_WORD,overallLineData.GetValue(overallLineData.FACTORY_NAME_KEY))
        self._WriteFile(filePath,fileName,result)


        return 
        
    # テンプレートファイルを読み込み
    def _ReadTemplateFile(self) -> list:
        lines = []
        abs_path = os.path.abspath(__file__)
        dir_path = os.path.dirname(abs_path)
        filePath = dir_path + "\\" + self.TEMPLATE_FILE_NAME
        with open(filePath, encoding="utf-8") as f:
            for line in f:
                lines.append(line.rstrip())
        return lines
    
    
    # 保存
    def _WriteFile(self,filePath,fileName,lines):
        os.chdir(os.path.dirname(__file__) + "/../")
        os.chdir(filePath)
        with open(fileName,"w", encoding="utf-8") as o:
            for line in lines:
                print(line,file=o)
        return
    

    # レシピ群の置き換え用の文字列を返す
    def _MakeRecipesText(
            self,overallData:OLineData
            ) -> list:
        
        # 返す用変数を作成
        result = ""

        # レシピリストの取得 
        recipeList = overallData.GetValue(overallData.RECIPE_LIST_KEY)

        # レシピごとの文章を加算
        for recipe in recipeList:
            result += self._MakeRecipeText(recipe[overallData.RECIPE_NAME_KEY])
        
        return result
    

    # レシピ単体の置き換え用文字列を返す
    def _MakeRecipeText(self,recipeName:str) -> str:
        
        # レシピデータ取得
        recipe = self._ReadRecipeFile(recipeName)

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
    def _MakeIndividualLinesText(self,overallData:OLineData) -> list:
        
        # 返す用変数を作成
        result = ""

        # 個別ラインリストの取得 
        lineList = overallData.GetValue(overallData.INDIVIDUAL_LINE_LIST)

        # 個別ラインごとの文章を加算
        for line in lineList:
            result += self._MakeIndividualLineText(line)
        
        return result
    

    # 個別ライン単体の置き換え用文字列を返す
    def _MakeIndividualLineText(self,iLineData:dict) -> str:
        
        overall = OLineData([])

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
    def _MakeFlowChart(self,overallData:OLineData) -> str:

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


    # レシピデータを読み込み
    def _ReadRecipeFile(self,recipeName:str) -> RecipeItem:
        recipes = RecipeReader()
        recipe = recipes.GetRecipe(recipeName)
        return recipe

