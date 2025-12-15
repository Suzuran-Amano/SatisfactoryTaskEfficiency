import json

class IndividualLineData:
    ### 定数 ###
    REPLACE_KEY_HEADER = "var_"
    LINE_NAME_KEY = "lineName"
    RECIPE_NAME_KEY = "recipeName"
    RECIPE_NUM_KEY = "recipeNum"
    PRODUCT_NAME_KEY = "productName"
    INPUT_NAME_KEY = "inputName"
    INPUT_NUM_KEY = "inputNum"
    OUTPUT_NAME_KEY = "outputName"
    OUTPUT_NUM_KEY = "outputNum"
    TOTAL_INPUT_KEY = "totalInput"
    TOTAL_OUTPUT_KEY = "totalOutput"


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
    
    def GetKeys(self):
        return self.value.keys()
    
    def GetReplaceKey(self,key):
        return self.REPLACE_KEY_HEADER + key
    
    # ファイルを出力
    def Output(self,path:str):
        # 書き込み
        jsonfile = open(path + '/' + self.GetLineName() + '.json', 'w',encoding='utf-8')
        json.dump(self.value, jsonfile, indent=4,ensure_ascii=False)

        return
    