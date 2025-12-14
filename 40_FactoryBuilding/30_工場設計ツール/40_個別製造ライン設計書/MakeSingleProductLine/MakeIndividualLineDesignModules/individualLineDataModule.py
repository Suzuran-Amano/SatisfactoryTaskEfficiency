
class IndividualLineData:
    # 定数
    LINE_NAME_KEY = "lineData"
    RECIPE_NAME_KEY = "recipeName"
    RECIPE_NUM_KEY = "recipeNum"


    # 変数
    value = []

    def __init__(self,jsonData):
        self.value = jsonData
        return
    
    # 個別製造ラインの名前を返す
    def GetLineName(self):
        return self.value[self.LINE_NAME_KEY]
    
    # レシピ名を返す
    def GetRecipeName(self):
        return self.value[self.RECIPE_NAME_KEY]
    
    # レシピ数を返す
    def GetRecipeNum(self):
        return self.value[self.RECIPE_NUM_KEY]