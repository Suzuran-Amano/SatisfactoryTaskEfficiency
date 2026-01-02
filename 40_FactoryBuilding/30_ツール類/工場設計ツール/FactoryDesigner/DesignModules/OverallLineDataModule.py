import os
import json

class OverallLineData:
    ### 定数 ###
    FILE_NAME = "OverallLineData.json"

    REPLACE_KEY_HEADER = "var_"
    
    FACTORY_NAME_KEY = "factoryName"

    RECIPE_LIST_KEY = "recipeList"
    RECIPE_NAME_KEY = "recipeName"
    INPUT_LIST_KEY = "inputList"
    OUTPUT_LIST_KEY = "outputList"
    ITEM_NAME_KEY = "itemName"
    ITEM_NUM_KEY = "itemNum"

    INDIVIDUAL_LINE_LIST = "individualLineList"
    INDIVIDUAL_LINE_NAME = "individualLineName"
    RECIPE_NUM_KEY = "recipeNum"
    
    INPUT_LINE_LIST = "inputlLineList"
    OUTPUT_LINE_LIST = "outputLineList"
    
    RELATIONSHIPS_KEY = "relationships"
    SUPPLYER_LINE_KEY = "supplierLine"
    DESTINATION_LINE_KEY = "destinationLine"
    SUPPLY_ITEM_KEY = "supplyItem"
    SUPPLY_NUM_KEY = "supplyNum"


    ### 変数 ###
    value = dict([])


    ### 関数 ###

    def __init__(self,value:dict):
        self.value = value
        return
    
    def GetValue(self,key:str):
        return self.value[key]
    
    # ファイルを出力
    def Output(self,path:str):

        outputPath = path + path.OVERALL_LINE_DIRECTORY_NAME
        
        # 書き込み
        os.makedirs(outputPath, exist_ok=True)
        jsonfile = open(outputPath + "\\" + self.FILE_NAME , 'w',encoding='utf-8')
        json.dump(self.value, jsonfile, indent=4,ensure_ascii=False)

        return
    