import os
import json

from .RecipeItemModule import RecipeItem


### 定数 ###

# 情報を保存しておくディレクトリの名前
INFOMATION_FILE_NAME = "01_InformationExtraction"

# レシピを保存しておくディレクトリの名前
RECIPES_DIRECTORY_NAME = "Recipes"


### 関数 ###

# レシピを追加
def GetRecipe(recipeName):
    os.chdir(_GetRecipesDirectory())
    openFile = open("./" + recipeName + ".json",'r', encoding="utf-8")
    return RecipeItem(json.load(openFile))

# レシピ集のディレクトリを返す
def _GetRecipesDirectory():

    while True:
        if os.path.isdir(os.getcwd() + "\\" + INFOMATION_FILE_NAME):
            break
        else:
            os.chdir('../')

    return os.getcwd() + "\\" + INFOMATION_FILE_NAME + "\\" + RECIPES_DIRECTORY_NAME
