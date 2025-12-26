import os
import sys
import json

from DesignModules import pathDataModule


# Constants
FACTORY_FILE_NAME_KEY = "FactoryData.json"

FACTORY_NAME_KEY = "factoryName"
USE_POWER_KEY = "usePower"

TOTAL_USE_POWER_NAME = "合計消費電力"


# 保存
def WriteFile(filePath,fileName,lines):
    os.makedirs(filePath, exist_ok=True)
    os.chdir(os.path.dirname(__file__) + "/../")
    os.chdir(filePath)
    with open(fileName,"w", encoding="utf-8") as o:
        for line in lines:
            print(line,file=o)
    return

### main ###

# パス情報を作成
pathData = pathDataModule.PathData(sys.argv)

# 工場データリスト作成
factoriesPath = os.path.dirname(os.path.dirname(pathData.GetPath()))
directories = os.listdir(factoriesPath) # ディレクトリ中のファイルを取得
directories.remove('10_工場設計手順書')
directories.remove('20_工場設計テンプレート')
directories.remove('30_ツール類')
directories.remove('90_集約情報')
for f in directories:
    if '.' in f :
        directories.remove(f)

# for f in directories:
    # print(f)


# 工場データリスト
factorieDataList = []
for f in directories:
    factoryDataPath = os.path.join(factoriesPath,f,FACTORY_FILE_NAME_KEY)
    if not(os.path.exists(factoryDataPath)) :
        continue
    jsonData = json.load(open(factoryDataPath,'r', encoding="utf-8"))
    factorieDataList.append(jsonData)

# for f in factorieDataList:
    # print(f[FACTORY_NAME_KEY])


# 工場データ配列を作成
factoryDataTextArray = []
for f in factorieDataList:
    factoryDataTextArray.append(f[FACTORY_NAME_KEY] + "," + str(f[USE_POWER_KEY]))


# 合計をリストに追加
totalPow = 0
for f in factorieDataList:
    totalPow += f[USE_POWER_KEY]
factoryDataTextArray.append(TOTAL_USE_POWER_NAME + "," + str(totalPow))


# 工場データを出力
filePath = pathData.GetPath()
fileName = pathData.GetFileName()
WriteFile(filePath,fileName,factoryDataTextArray)


