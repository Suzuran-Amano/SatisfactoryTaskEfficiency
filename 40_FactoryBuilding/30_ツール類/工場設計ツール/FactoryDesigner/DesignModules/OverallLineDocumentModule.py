import os

from . import pathDataModule
from . import InfomationReaderModule as InfoReader
from . import RecipeItemModule
from . import OverallLineDataModule as OLineDataModule
from . import DocumentMakerModule 


# 全体造製ライン設計書を作成、出力するクラス
class OverallLineDocument(DocumentMakerModule.DocumentMaker):

    # 定数
    TEMPLATE_FILE_NAME = './全体製造ライン設計書_var_factoryName.md'
    OUTPUT_FILE_NAME = '全体製造ライン設計書_var_factoryName.md'

    FACTORY_NAME_KEY_WORD = "var_factoryName"
    RECIPIES_KEY_WORD = "var_recipies"
    LINES_KEY_WORD = "var_lines"
    FLOWCHART_KEY_WORD = "var_flowChart"


    # 書類の作成と出力を行う関数
    def MakeDocument(
            self,
            pathData : pathDataModule.PathData,
            oLineData : OLineDataModule.OverallLineData):

        # 全体ラインテンプレートを読み込み
        templateLines = self._ReadTemplateFile(self.TEMPLATE_FILE_NAME)

        # 置換用データを作成
        recipeText = self._MakeRecipesText(oLineData)
        linesText = self._MakeIndividualLinesText(oLineData)
        flowchartText = self._MakeFlowChart(oLineData)

        # 置き換え
        result = []
        for line in templateLines :
            text = line
            text = text.replace(self.RECIPIES_KEY_WORD,recipeText)
            text = text.replace(self.LINES_KEY_WORD,linesText)
            text = text.replace(self.FLOWCHART_KEY_WORD,flowchartText)
            text = text.replace(self.FACTORY_NAME_KEY_WORD,oLineData.GetValue(OLineDataModule.FACTORY_NAME_KEY))
            result.append(text)

        # print(result)

        # 書類の出力
        self._WriteFile(pathData,oLineData, result)

        return 
       
        
    # 書類データを保存
    def _WriteFile(
            self,
            pathData : pathDataModule.PathData,
            oLineData : OLineDataModule.OverallLineData,
            lines : list
            ):

        outputPath = pathData.GetPath() + "\\" + pathDataModule.OVERALL_LINE_DIRECTORY_NAME
        fileName = self._Replace(self.OUTPUT_FILE_NAME,oLineData)

        super()._WriteFile(outputPath,fileName,lines)

        return
    

    # すべての行の置き換え
    def _AllLineReplace(
            self,
            lines : list,
            oLineData : OLineDataModule.OverallLineData
            ) -> list:
        
        for index in range(len(lines)):
            lines[index] = self._Replace(lines[index],oLineData)

        return lines

    
    # 置き換え
    def _Replace(
            self,
            text : str,
            oLineData : OLineDataModule.OverallLineData
            ) -> str:
        
        for key in oLineData.GetKeys():
            text = text.replace(oLineData.GetReplaceKey(key),str(oLineData.GetValue(key)))

        return text


    # レシピ群の置き換え用の文字列を返す
    def _MakeRecipesText(
            self,overallData:OLineDataModule.OverallLineData
            ) -> list:
        
        # 返す用変数を作成
        result = ""

        # レシピリストの取得 
        recipeList = overallData.GetValue(OLineDataModule.RECIPE_LIST_KEY)

        # レシピごとの文章を加算
        for recipe in recipeList:
            result += self._MakeRecipeText(recipe[OLineDataModule.RECIPE_NAME_KEY])
        
        return result
    

    # レシピ単体の置き換え用文字列を返す
    def _MakeRecipeText(self,recipeName:str) -> str:
        
        # レシピデータ取得
        recipe = InfoReader.GetRecipe(recipeName)

        # ヘッダー
        result = "### " + recipe.GetValue(RecipeItemModule.RECIPE_NAME_KEY) + "\n"
        result += "|I/O|物品名|要求数|\n"
        result += "|---|---|---|\n"

        
        # input 
        items = recipe.GetValue(RecipeItemModule.INPUT_KEY)
        for item in items:
            result += "|input|" + str(item[RecipeItemModule.ITEM_NAME_KEY]) + "|" + str(item[RecipeItemModule.ITEM_NUM_KEY]) + "|\n"

        result += "|---|---|---|\n"

        # input 
        items = recipe.GetValue(RecipeItemModule.OUTPUT_KEY)
        for item in items:
            result += "|output|" + str(item[RecipeItemModule.ITEM_NAME_KEY]) + "|" + str(item[RecipeItemModule.ITEM_NUM_KEY]) + "|\n"

        return result
    

    # 個別ラインリストの置き換え用の文字列を返す
    def _MakeIndividualLinesText(self,overallData:OLineDataModule.OverallLineData) -> list:
        
        # 返す用変数を作成
        result = ""

        # 個別ラインリストの取得 
        lineList = overallData.GetValue(OLineDataModule.INDIVIDUAL_LINE_LIST)

        # 個別ラインごとの文章を加算
        for line in lineList:
            result += self._MakeIndividualLineText(line)
        
        return result
    

    # 個別ライン単体の置き換え用文字列を返す
    def _MakeIndividualLineText(self,iLineData:dict) -> str:
        
        # タイトル
        result = "### " + iLineData[OLineDataModule.INDIVIDUAL_LINE_NAME] + "\n"
        result += "\n"
        
        # 基本情報
        result += "レシピ名 : " + iLineData[OLineDataModule.RECIPE_NAME_KEY] + "  \n"
        result += "レシピ数 : " + str(iLineData[OLineDataModule.RECIPE_NUM_KEY]) + "\n"
        result += "\n"
        
        # ヘッダー
        result += "|I/O|物品名|要求数|\n"
        result += "|---|---|---|\n"

        
        # input 
        items = iLineData[OLineDataModule.INPUT_LIST_KEY]
        for item in items:
            result += "|input|" + str(item[OLineDataModule.ITEM_NAME_KEY]) + "|" + str(item[OLineDataModule.ITEM_NUM_KEY]) + "|\n"

        result += "|---|---|---|\n"

        # output 
        items = iLineData[OLineDataModule.OUTPUT_LIST_KEY]
        for item in items:
            result += "|output|" + str(item[OLineDataModule.ITEM_NAME_KEY]) + "|" + str(item[OLineDataModule.ITEM_NUM_KEY]) + "|\n"

        result += "\n"
        result += "\n"

        return result


    # フローチャート作成
    def _MakeFlowChart(self,overallData:OLineDataModule.OverallLineData) -> str:

        result = ""
        inputList = overallData.GetValue(OLineDataModule.INPUT_LINE_LIST)
        lineList = overallData.GetValue(OLineDataModule.INDIVIDUAL_LINE_LIST)
        outputList = overallData.GetValue(OLineDataModule.OUTPUT_LINE_LIST)
        relationships = overallData.GetValue(OLineDataModule.RELATIONSHIPS_KEY)
            
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
            result += line[OLineDataModule.INDIVIDUAL_LINE_NAME] + "\n"
        result += "\n"

        # output
        result += "subgraph Output\n"
        for outputName in outputList:
            result += "    " + outputName +"([" + outputName + "])\n"
        result += "end\n\n"


        # flow
        for relation in relationships:
            supplierLine = relation[OLineDataModule.SUPPLYER_LINE_KEY]
            destinationLine = relation[OLineDataModule.DESTINATION_LINE_KEY]
            supplyItem = relation[OLineDataModule.SUPPLY_ITEM_KEY]
            supplyNum = relation[OLineDataModule.SUPPLY_NUM_KEY]
            result += supplierLine + "-->|" + supplyItem + str(supplyNum) + "|" + destinationLine + "\n"

        result += "```\n"
        
        return result
