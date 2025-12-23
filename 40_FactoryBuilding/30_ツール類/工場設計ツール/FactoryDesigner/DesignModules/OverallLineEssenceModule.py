import json

class OverallLineEssence:
    ### 定数 ###
    FACTORY_NAME_KEY = "factoryName"

    RECIPE_LIST_KEY = "recipeList"
    RECIPE_NAME_KEY = "recipeName"
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
    
    