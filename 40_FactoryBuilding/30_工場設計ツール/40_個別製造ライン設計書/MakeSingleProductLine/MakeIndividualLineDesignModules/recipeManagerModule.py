import os
import json


# レシピ集
class RecipeReader:

    ### 定数 ###

    # 情報を保存しておくディレクトリの名前
    INFOMATION_FILE_NAME = "01_InformationExtraction"

    # レシピを保存しておくディレクトリの名前
    RECIPES_DIRECTORY_NAME = "Recipes"


    ### 関数 ###

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

    ### 定数

    # 配列のキー定数
    RECIPE_NAME_KEY = "recipeName"
    PRODUCT_NAME_KEY = "productName"
    INPUT_KEY = "input"
    OUTPUT_KEY = "output"
    ITEM_NAME_KEY = "itemName"
    ITEM_NUM_KEY = "itemNum"


    ### 変数 ###

    # Jsonファイル内のデータ
    jsonData = []

    
    # コンストラクタ
    def __init__(self,data):
        self.jsonData = data
        return


    # レシピ名
    def GetRecipeName(self):
        return self.jsonData[self.RECIPE_NAME_KEY]
    
    # 製造機器名
    def GetProductName(self):
        return self.jsonData[self.PRODUCT_NAME_KEY]
    
    
    # 加工元アイテムのリスト
    def GetInputItemList(self):
        return self.jsonData[self.INPUT_KEY]
    
    # 加工元アイテムのリスト長
    def GetInputItemLength(self):
        return len(self.GetInputItemList())
    
    # 加工元アイテムの名前
    def GetInputItemName(self,index):
        if index >= self.GetInputItemLength():
            return None
        return self.GetInputItemList(index)[self.ITEM_NAME_KEY]
    
    # 加工元アイテムの1分当たりの個数
    def GetInputItemNum(self,index):
        if index >= self.GetInputItemLength():
            return None
        return self.GetInputItemList(index)[self.ITEM_NUM_KEY]


    # 加工後アイテムのリスト
    def GetOutputItemList(self):
        return self.jsonData[self.OUTPUT_KEY]
    
    # 加工後アイテムのリスト長
    def GetOutputItemLength(self):
        return len(self.GetOutputItemList())
    
    # 加工後アイテムの名前
    def GetOutputItemName(self,index):
        if index >= self.GetOutputItemLength():
            return None
        return self.GetOutputItemList(index)[self.ITEM_NAME_KEY]
    
    # 加工後アイテムの1分当たりの個数
    def GetOutputItemNum(self,index):
        if index >= self.GetOutputItemLength():
            return None
        return self.GetOutputItemList(index)[self.ITEM_NUM_KEY]
    
