import os

from . import pathDataModule
from .BasicData import BasicDataReader
from .BasicData import RecipeData
from .BasicData import ResourceData
from . import OverallLineDataModule as OLineDataModule
from . import DocumentMakerModule 


# 全体造製ライン設計書を作成、出力するクラス
class OverallLineDocument(DocumentMakerModule.DocumentMaker):

    # 定数
    TEMPLATE_FILE_NAME = './全体製造ライン設計書_var_factoryName.md'
    OUTPUT_FILE_NAME = '全体製造ライン設計書_var_factoryName.md'

    FACTORY_NAME_KEY_WORD = "var_factoryName"
    PRODUCTION_KEY = "production"
    RECIPIES_KEY = "recipies"
    INDIVIDUAL_LINES_KEY = "lines"
    FLOWCHART_KEY = "flowChart"


    # 書類の作成と出力を行う関数
    def MakeDocument(
            self,
            pathData : pathDataModule.PathData,
            oLineData : OLineDataModule.OverallLineData):
        
        # 全体ラインテンプレートを読み込み
        templateLines = self._ReadTemplateFile(self.TEMPLATE_FILE_NAME)
        templateLines = self._DuplicateProductLines(templateLines,oLineData)

        # 置換用データを作成
        replaceDict = self._MakeReplaceDict(oLineData)
        
        # 置き換え
        result = self._AllLineReplace(templateLines,replaceDict)
        
        # 書類の出力
        self._WriteFile(pathData,oLineData, result)

        return
    

    # 置き換え用辞書の作成
    def _MakeReplaceDict(
            self,
            oLineData : OLineDataModule.OverallLineData
            ) -> dict:
        
        replaceDict = oLineData.GetValueDict().copy()

        # 一時産品リストのキーを削除
        if OLineDataModule.PRODUCTION_LIST in replaceDict:
            replaceDict.pop(OLineDataModule.PRODUCTION_LIST)
        replaceDict = self._AddProductionReplaceDict(replaceDict,oLineData,OLineDataModule.RESOURCE_NAME)
        replaceDict = self._AddProductionReplaceDict(replaceDict,oLineData,OLineDataModule.TOTAL_RESOURCE_OUTPUT_NUM)
        
        replaceDict[self.PRODUCTION_KEY] = self._MakeProductLines(oLineData)
        replaceDict[self.RECIPIES_KEY] = self._MakeRecipesText(oLineData)
        replaceDict[self.INDIVIDUAL_LINES_KEY] = self._MakeIndividualLinesText(oLineData)
        replaceDict[self.FLOWCHART_KEY] = self._MakeFlowChart(oLineData)

        
        return replaceDict
    

    # Production 関係の置き換え用辞書作成
    def _AddProductionReplaceDict(
            self,
            replaceDict : dict,
            oLineData : OLineDataModule.OverallLineData,
            key : str
            ) -> dict:
        
        # 一時産品のリストを取得
        productionList = oLineData.GetValue(OLineDataModule.PRODUCTION_LIST)
        if productionList == None:
            return replaceDict

        # 一時産品の数だけ繰り返す
        for i in range(len(productionList)):

            # キーを作成
            replaceKey = OLineDataModule.PRODUCTION_LIST + "." + key + str(i+1)

            # 置き換え後の値を作成
            value = productionList[i][key]
            
            # 辞書に登録
            replaceDict[replaceKey] = value

        return replaceDict
       
        
    # 書類データを保存
    def _WriteFile(
            self,
            pathData : pathDataModule.PathData,
            oLineData : OLineDataModule.OverallLineData,
            lines : list
            ):

        outputPath = pathData.GetPath() + "\\" + pathDataModule.OVERALL_LINE_DIRECTORY_NAME
        fileName = self._Replace(self.OUTPUT_FILE_NAME,oLineData.GetValueDict())

        super()._WriteFile(outputPath,fileName,lines)

        return
    

    # 資源群を複製する
    def _DuplicateProductLines(
            self,
            lines,
            oLineData : OLineDataModule.OverallLineData
            ):
        
        keys = []

        productionList = oLineData.GetValue(OLineDataModule.PRODUCTION_LIST)
        # リストがないなら、複製しない
        if productionList == None : 
            return lines
        
        length = len(productionList)
        keys.append(self._GetReplaceKey(OLineDataModule.PRODUCTION_LIST + "." + OLineDataModule.RESOURCE_NAME))
        keys.append(self._GetReplaceKey(OLineDataModule.PRODUCTION_LIST + "." + OLineDataModule.TOTAL_RESOURCE_OUTPUT_NUM))

        return self._DuplicateLines(lines,length,keys)
    
    # 資源群の置き換え用の文字列を返す
    def _MakeProductLines(
            self,
            overallData:OLineDataModule.OverallLineData
            ) -> str:
        
        # 返す用変数を作成
        result = "## 資源\n"
        result += "|資源名|産出量|\n"
        result += "|---|---|\n"

        # 資源リストの取得 
        resourceList = overallData.GetValue(OLineDataModule.PRODUCTION_LIST)
        if resourceList == None:
            return ""
        if len(resourceList) == 0:
            return ""
        
        # 資源ごとに合算
        resourceDict = {}
        for resource in resourceList:
            if resource[OLineDataModule.RESOURCE_NAME] in resourceDict:
                resourceDict[resource[OLineDataModule.RESOURCE_NAME]] += resource[OLineDataModule.TOTAL_RESOURCE_OUTPUT_NUM]
            else : 
                resourceDict[resource[OLineDataModule.RESOURCE_NAME]] = resource[OLineDataModule.TOTAL_RESOURCE_OUTPUT_NUM]

        # レシピごとの文章を加算
        for key,item in resourceDict.items():
            result += "|" + key + "|" + str(item) + "|\n"

        
        result += "\n\n"

        return result


    # レシピ群の置き換え用の文字列を返す
    def _MakeRecipesText(
            self,overallData:OLineDataModule.OverallLineData
            ) -> str:
        
        # 返す用変数を作成
        result = "## 使用レシピ\n"

        # レシピリストの取得 
        recipeList = overallData.GetValue(OLineDataModule.RECIPE_LIST_KEY)
        if recipeList == None:
            return ""
        if len(recipeList) == 0:
            return ""

        # レシピごとの文章を加算
        for recipe in recipeList:
            result += self._MakeRecipeText(recipe[OLineDataModule.RECIPE_NAME_KEY])
        
        result += "\n\n"

        return result
    

    # レシピ単体の置き換え用文字列を返す
    def _MakeRecipeText(self,recipeName:str) -> str:
        
        # レシピデータ取得
        recipe = BasicDataReader.GetRecipe(recipeName)

        # ヘッダー
        result = "### " + recipe.GetValue(RecipeData.RECIPE_NAME_KEY) + "\n"
        result += "|I/O|物品名|要求数|\n"
        result += "|---|---|---|\n"

        
        # input 
        items = recipe.GetValue(RecipeData.INPUT_KEY)
        for item in items:
            result += "|input|" + str(item[RecipeData.ITEM_NAME_KEY]) + "|" + str(item[RecipeData.ITEM_NUM_KEY]) + "|\n"

        result += "|---|---|---|\n"

        # input 
        items = recipe.GetValue(RecipeData.OUTPUT_KEY)
        for item in items:
            result += "|output|" + str(item[RecipeData.ITEM_NAME_KEY]) + "|" + str(item[RecipeData.ITEM_NUM_KEY]) + "|\n"

        return result
    

    # 個別ラインリストの置き換え用の文字列を返す
    def _MakeIndividualLinesText(self,overallData:OLineDataModule.OverallLineData) -> list:
        
        # 返す用変数を作成
        result = "## 必要製造ライン\n"

        # 個別ラインリストの取得 
        lineList = overallData.GetValue(OLineDataModule.INDIVIDUAL_LINE_LIST)
        if lineList == None:
            return ""
        if len(lineList) == 0:
            return ""

        # 個別ラインごとの文章を加算
        for line in lineList:
            result += self._MakeIndividualLineText(line)
        
        result += "\n\n"
        
        return result
    

    # 個別ライン単体の置き換え用文字列を返す
    def _MakeIndividualLineText(self,iLineData:dict) -> str:
        
        # タイトル
        result = "### " + iLineData[OLineDataModule.INDIVIDUAL_LINE_NAME] + "\n"
        result += "\n"
        
        # 基本情報
        result += "レシピ名 : " + iLineData[OLineDataModule.RECIPE_NAME_KEY] + "  \n"
        if OLineDataModule.RECIPE_NUM_KEY in iLineData:  # 辞書にキーがある場合
            result += "レシピ数 : " + str(iLineData[OLineDataModule.RECIPE_NUM_KEY]) + "\n"
        else:
            result += iLineData[OLineDataModule.BLUEPRINT_NAME]  # 青写真名
            result += str(iLineData[OLineDataModule.BLUEPRINT_NUM])  # 青写真数
        
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
        if inputList != None:
            result += "subgraph Input\n"
            for inputName in inputList:
                result += "    " + inputName +"([" + inputName + "])\n"
            result += "end\n\n"

        # product
        if lineList != None:
            for line in lineList:
                result += line[OLineDataModule.INDIVIDUAL_LINE_NAME] + "\n"
            result += "\n"

        # output
        if outputList != None:
            result += "subgraph Output\n"
            for outputName in outputList:
                result += "    " + outputName +"([" + outputName + "])\n"
            result += "end\n\n"


        # flow
        if relationships != None:
            for relation in relationships:
                supplierLine = relation[OLineDataModule.SUPPLYER_LINE_KEY]
                destinationLine = relation[OLineDataModule.DESTINATION_LINE_KEY]
                supplyItem = relation[OLineDataModule.SUPPLY_ITEM_KEY]
                supplyNum = relation[OLineDataModule.SUPPLY_NUM_KEY]
                result += supplierLine + "-->|" + supplyItem + "|" + destinationLine + "\n"

        result += "```\n"
        
        return result
