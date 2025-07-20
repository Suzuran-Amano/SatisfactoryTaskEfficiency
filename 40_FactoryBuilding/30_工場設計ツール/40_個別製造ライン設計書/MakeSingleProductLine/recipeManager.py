import os
import json


# レシピ集
class RecipeReader:

    # 定数

    # 情報を保存しておくディレクトリの名前
    INFOMATION_FILE_NAME = "01_InformationExtraction"

    # レシピを保存しておくディレクトリの名前
    RECIPES_DIRECTORY_NAME = "Recipes"


    # レシピ集のディレクトリを返す
    def GetRecipesDirectory(self):
    
        while True:
            if os.path.isdir(os.getcwd() + "\\" + self.INFOMATION_FILE_NAME):
                break
            else:
                os.chdir('../')

        return os.getcwd() + "\\" + self.INFOMATION_FILE_NAME + "\\" + self.RECIPES_DIRECTORY_NAME


    # レシピを追加
    def GetRecipe(self,recipeName):
        os.chdir(self.GetRecipesDirectory())
        openFile = open("./" + recipeName + ".json",'r', encoding="utf-8")
        return RecipeItem(json.load(openFile))
        


# 単一のレシピ
class RecipeItem:

    RECIPE_NAME_KEY = "recipeName"
    PRODUCT_NAME_KEY = "productName"
    INPUT_KEY = "input"
    OUTPUT_KEY = "output"
    ITEM_NAME_KEY = "itemName"
    ITEM_NUM_KEY = "itemNum"

    # Jsonファイル内のデータ
    jsonData = []

    
    # コンストラクタ
    def __init__(self,data):
        self.jsonData = data
        return

    def GetRecipeName(self):
        return self.jsonData[self.RECIPE_NAME_KEY]
    
    def GetProductName(self):
        return self.jsonData[self.PRODUCT_NAME_KEY]
        
    def GetInputItemList(self):
        return self.jsonData[self.INPUT_KEY]
    
    def GetOutputItemList(self):
        return self.jsonData[self.OUTPUT_KEY]
    
