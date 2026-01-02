import os
import json

from .pathDataModule import PathData

class IndividualLineData:
    # 定数
    FILE_NAME = "IndividualLineData_var_lineName.json"
    LINE_NAME_REPLACE_TEXT = "var_lineName"

    REPLACE_KEY_HEADER = "var_"
    LINE_NAME_KEY = "lineName"
    RECIPE_NAME_KEY = "recipeName"
    RECIPE_NUM_KEY = "recipeNum"
    PRODUCT_NAME_KEY = "productName"
    TOTAL_USE_POWER_KEY = "totalUsePower"
    INPUT_NAME_KEY = "inputName"
    INPUT_NUM_KEY = "inputNum"
    OUTPUT_NAME_KEY = "outputName"
    OUTPUT_NUM_KEY = "outputNum"
    TOTAL_INPUT_KEY = "totalInput"
    TOTAL_OUTPUT_KEY = "totalOutput"

    COST_LIST_KEY = "costList"
    ITEM_NAME_KEY = "itemName"
    ITEM_NUM_KEY = "itemNum"
    SUPPLY_POWER_KEY = "supplyPower"


    ### 変数 ###
    value = dict([])


    ### 関数 ###

    
    def Append(self,key,val):
        self.value[key] = val
        return
    
    def GetLineName(self):
        return self.value[self.LINE_NAME_KEY]
    
    def GetRecipeName(self):
        return self.value[self.RECIPE_NAME_KEY]
        
    def GetRecipeNum(self):
        return self.value[self.RECIPE_NUM_KEY]
        
    def GetProductName(self):
        return self.value[self.PRODUCT_NAME_KEY]
    
    def GetTotalUsePower(self):
        return self.value[self.TOTAL_USE_POWER_KEY]
    

    def GetInputName(self,index):
        print(self.value)
        return self.value[self.INPUT_NAME_KEY + str(index)]
    
    def GetInputNum(self,index):
        return self.value[self.INPUT_NUM_KEY + str(index)]
    

    def GetOutputName(self,index):
        return self.value[self.OUTPUT_NAME_KEY + str(index)]
    
    def GetOutputNum(self,index):
        return self.value[self.OUTPUT_NUM_KEY + str(index)]
    
    
    def GetTotalInput(self):
        return self.value[self.TOTAL_INPUT_KEY]
    
    def GetTotalOutput(self):
        return self.value[self.TOTAL_OUTPUT_KEY]
    

    def GetCostList(self):
        return self.value[self.COST_LIST_KEY]
    
    def GetSupplyPower(self):
        if self.SUPPLY_POWER_KEY in self.value:
            return self.value[self.SUPPLY_POWER_KEY]
        else:
            return 0

    
    def GetKeys(self):
        return self.value.keys()
    
    def GetReplaceKey(self,key):
        return self.REPLACE_KEY_HEADER + key
    
    # ファイルを出力
    def Output(self,path:str):
        
        # パス計算
        outputPath = path + PathData().INDIVIDUAL_LINE_DIRECTORY_NAME
        
        # ファイル名作成
        fileName = self.FILE_NAME.replace(self.LINE_NAME_REPLACE_TEXT,self.GetLineName())

        # 書き込み
        os.makedirs(outputPath, exist_ok=True)
        jsonfile = open(outputPath + "\\" + fileName , 'w',encoding='utf-8')
        json.dump(self.value, jsonfile, indent=4,ensure_ascii=False)

        return
    