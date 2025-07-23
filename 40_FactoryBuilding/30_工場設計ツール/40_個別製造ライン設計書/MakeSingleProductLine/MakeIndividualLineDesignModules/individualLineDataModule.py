class IndividualLineData:
    # 定数
    RECIPE_NAME_KEY = "recipeName"
    RECIPE_NUM_KEY = "recipeNum"


    # 変数
    value = []

    def __init__(self,jsonData):
        self.value = jsonData
        return
    
    def GetRecipeName(self):
        return self.value[self.RECIPE_NAME_KEY]
        
    def GetRecipeNum(self):
        return self.value[self.RECIPE_NUM_KEY]