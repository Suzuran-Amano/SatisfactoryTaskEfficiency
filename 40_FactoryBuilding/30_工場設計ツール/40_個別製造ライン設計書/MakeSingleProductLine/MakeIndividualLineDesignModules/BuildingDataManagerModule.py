import os
import json


# 設備集
class BuildingDataReader:

    ### 定数 ###

    # 情報を保存しておくディレクトリの名前
    INFOMATION_FILE_NAME = "01_InformationExtraction"

    # 設備情報を保存しておくディレクトリの名前
    BUILDING_DIRECTORY_NAME = "Building"


    ### 関数 ###

    # 設備集のディレクトリを返す
    def GetBuildingsDirectory(self):
    
        while True:
            if os.path.isdir(os.getcwd() + "\\" + self.INFOMATION_FILE_NAME):
                break
            else:
                os.chdir('../')

        return os.getcwd() + "\\" + self.INFOMATION_FILE_NAME + "\\" + self.BUILDING_DIRECTORY_NAME

    # 設備情報を追加
    def GetBuildingInfo(self,buildingName):
        os.chdir(self.GetBuildingsDirectory())
        openFile = open("./" + buildingName + ".json",'r', encoding="utf-8")
        loadedfile = json.load(openFile)
        # print(buildingName)
        # print(loadedfile)
        return BuildingDataItem(loadedfile)
        


# 単一の設備情報
class BuildingDataItem:

    ### 定数

    # 配列のキー定数
    BUILDING_NAME_KEY = "buildingName"
    USE_POWER_KEY = "usePower"
    COST_KEY = "cost"


    ### 変数 ###

    # Jsonファイル内のデータ
    jsonData = []

    
    # コンストラクタ
    def __init__(self,data):
        self.jsonData = data
        return


    # 設備名
    def GetBuildingName(self):
        return self.jsonData[self.BUILDING_NAME_KEY]
    
    # 製造機器名
    def GetUsePowerName(self):
        return self.jsonData[self.USE_POWER_KEY]
    
    
    # 加工元アイテムのリスト
    def GetCostList(self):
        return self.jsonData[self.COST_KEY]
    
    # 加工元アイテムのリスト長
    def GetCostLength(self):
        return len(self.GetCostList())
    
    # 加工元アイテムの名前
    def GetCostName(self,index):
        if index >= self.GetCostLength():
            return None
        return self.GetCostList(index)[self.COST_KEY]
    
    # 加工元アイテムの1分当たりの個数
    def GetCostNum(self,index):
        if index >= self.GetCostLength():
            return None
        return self.GetCostList(index)[self.COST_KEY]
    
