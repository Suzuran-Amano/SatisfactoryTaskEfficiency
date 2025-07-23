

class ReplaceData:
    # 定数
    RECIPE_NAME_KEY = "recipeName"
    RECIPE_NUM_KEY = "recipeNum"
    PRODUCT_NAME_KEY = "productName"
    INPUT_NAME_KEY = "inputName"
    INPUT_NUM_KEY = "inputNum"
    OUTPUT_NAME_KEY = "outputName"
    OUTPUT_NUM_KEY = "outputNum"
    TOTAL_INPUT_KEY = "totalInput"
    TOTAL_OUTPUT_KEY = "totalOutput"


    # 変数
    value = dict([])

    def Append(self,key,val):
        self.value[key] = val
        return
    
    def GetRecipeName(self):
        return self.value[self.RECIPE_NAME_KEY]
        
    def GetRecipeNum(self):
        return self.value[self.RECIPE_NUM_KEY]
        
    def GetProductName(self):
        return self.value[self.PRODUCT_NAME_KEY]
    
    def GetInputName(self):
        return self.value[self.INPUT_NAME_KEY]
    
    def GetInputNum(self):
        return self.value[self.INPUT_NUM_KEY]
    
    def GetOutputName(self):
        return self.value[self.OUTPUT_NAME_KEY]
    
    def GetOutputNum(self):
        return self.value[self.OUTPUT_NUM_KEY]
    
    def GetTotalInput(self):
        return self.value[self.TOTAL_INPUT_KEY]
    
    def GetTotalOutput(self):
        return self.value[self.TOTAL_OUTPUT_KEY]
    
    def GetKeys(self):
        return self.value.keys()
    