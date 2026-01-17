import os
import json

from .RecipeData import RecipeData
from .BuildingData import BuildingData
from .ResourceData import ResourceData
from .BlueprintData import BlueprintData


### 定数 ###

# 情報を保存しておくディレクトリの名前
INFOMATION_FILE_NAME = "01_InformationExtraction"

# 各情報を保存しておくディレクトリの名前
RECIPES_DIRECTORY_NAME = "Recipes"
BUILDING_DIRECTORY_NAME = "Building"
RESOURCE_DIRECTORY_NAME = "Resources"
BLUEPRINT_DIRECTORY_NAME = "Blueprint"


### 関数 ###

# レシピを追加
def GetRecipe(recipeName:str):
    return RecipeData(_OpenFile(_GetRecipesDirectoryPath(),recipeName))

# 設備情報を追加
def GetBuildingData(buildingName:str):
    return BuildingData(_OpenFile(_GetBuildingsDirectoryPath(),buildingName))

# 資源情報を追加
def GetResourceData(resourceName:str):
    return ResourceData(_OpenFile(_GetResourcesDirectoryPath(),resourceName))

# 青写真情報を追加
def GetBlueprintData(resourceName:str):
    return ResourceData(_OpenFile(_GetBlueprintDirectoryPath(),resourceName))

# ファイルを開く
def _OpenFile(dirPath:str,fileName:str):
    openFile = open(dirPath + "\\" + fileName + ".json",'r', encoding="utf-8")
    return json.load(openFile)


# レシピ集のディレクトリを返す
def _GetRecipesDirectoryPath():
    return _GetInfomationDirectoryPath() + "\\" + RECIPES_DIRECTORY_NAME

# 設備集のディレクトリを返す
def _GetBuildingsDirectoryPath():
    return _GetInfomationDirectoryPath() + "\\" + BUILDING_DIRECTORY_NAME

# 資源集のディレクトリを返す
def _GetResourcesDirectoryPath():
    return _GetInfomationDirectoryPath() + "\\" + RESOURCE_DIRECTORY_NAME

# 資源集のディレクトリを返す
def _GetBlueprintDirectoryPath():
    return _GetInfomationDirectoryPath() + "\\" + BLUEPRINT_DIRECTORY_NAME

# 情報ディレクトリのパスを返す
def _GetInfomationDirectoryPath() -> str:
    path = __file__
    while True:
        if os.path.isdir(path + "\\" + INFOMATION_FILE_NAME):
            return path + "\\" + INFOMATION_FILE_NAME
        else:
            path = os.path.dirname(path)
    return

