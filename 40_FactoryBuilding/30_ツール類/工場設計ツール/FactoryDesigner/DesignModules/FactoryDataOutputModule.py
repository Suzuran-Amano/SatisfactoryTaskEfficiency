import json
from DesignModules import IndividualLineDataModule as ILineData
from DesignModules import OverallLineDataModule as OLineData
from DesignModules.BasicData import BasicDataReader
from DesignModules.BasicData import BlueprintData

def _CalculateIndividualLineCosts(iLineDataList, costList, usePow, supplyPower):
    """
    個別製造ラインからコストを集計する関数

    Args:
        iLineDataList: 個別ラインデータリスト
        costList: コストリスト
        usePow: 消費電力
        supplyPower: 供給電力

    Returns:
        costList, usePow, supplyPower: 更新された値
    """
    for iLineData in iLineDataList:
        usePow += iLineData.GetValue(ILineData.TOTAL_USE_POWER_KEY)
        supplyPower += iLineData.GetValue(ILineData.SUPPLY_POWER_KEY)

        itemNameKey = ILineData.ITEM_NAME_KEY
        itemNumKey = ILineData.ITEM_NUM_KEY
        for cost in iLineData.GetValue(ILineData.COST_LIST_KEY):
            itemName = cost[itemNameKey]
            itemNum = cost[itemNumKey]
            costList = _AddCost(costList,itemName,itemNum)

    return costList, usePow, supplyPower

def _CalculateStationCost(oLineData, costList):
    """
    鉄道駅のコストを追加する関数

    Args:
        oLineData: 全体ラインデータオブジェクト
        costList: コストリスト

    Returns:
        costList: 更新されたコストリスト
    """
    stationNum = oLineData.GetValue(OLineData.STATION_NUM)
    if stationNum == 0:
        return costList

    blueprintData = [
        BasicDataReader.GetBlueprintData("鉄道駅4"),
        BasicDataReader.GetBlueprintData("駅橋"),
        BasicDataReader.GetBlueprintData("駅用スマート整流機"),
        BasicDataReader.GetBlueprintData("搬出橋"),
        BasicDataReader.GetBlueprintData("搬入橋ジャンクション")
        ]
    
    for blueprint in blueprintData:
        costs = blueprint.GetValue(BlueprintData.COST)
        for cost in costs:
            itemName = cost[BlueprintData.ITEM_NAME]
            itemNum = cost[BlueprintData.AMOUNT] * stationNum
            costList = _AddCost(costList,itemName,itemNum)

    return costList

def _CalculateFloorCost(oLineData, costList):
    """
    床のコストを追加する関数

    Args:
        oLineData: 全体ラインデータオブジェクト
        costList: コストリスト

    Returns:
        costList: 更新されたコストリスト
    """
    totalWidth = oLineData.GetValue(OLineData.TOTAL_WIDTH_KEY)
    depth = 22
    floorArea = totalWidth * depth
    blueprintData = BasicDataReader.GetBlueprintData("土台")
    costs = blueprintData.GetValue(BlueprintData.COST)
    for cost in costs:
        itemName = cost[BlueprintData.ITEM_NAME]
        itemNum = cost[BlueprintData.AMOUNT] * floorArea
        costList = _AddCost(costList,itemName,itemNum)

    return costList

def _AddCost(
        costList : list,
        itemName : str,
        itemNum 
        ):
    
    if itemName in costList:
        costList[itemName] += itemNum
    else:
        costList[itemName] = itemNum

    return costList


def _CalculateWallCost(oLineData, costList):
    """
    壁のコストを追加する関数

    Args:
        oLineData: 全体ラインデータオブジェクト
        costList: コストリスト

    Returns:
        costList: 更新されたコストリスト
    """
    totalWidth = oLineData.GetValue(OLineData.TOTAL_WIDTH_KEY)
    depth = 22
    perimeter = (totalWidth + depth) * 2
    height = 6
    wallArea = perimeter * height
    blueprintData = BasicDataReader.GetBlueprintData("壁")
    costs = blueprintData.GetValue(BlueprintData.COST)
    for cost in costs:
        itemName = cost[BlueprintData.ITEM_NAME]
        itemNum = cost[BlueprintData.AMOUNT] * wallArea
        if itemName in costList:
            costList[itemName] += itemNum
        else:
            costList[itemName] = itemNum

    return costList

def OutputFactoryData(pathData, oLineData, iLineDataList):
    """
    工場データを計算してJSONファイルに出力する関数

    Args:
        pathData: パスデータオブジェクト
        oLineData: 全体ラインデータオブジェクト
        iLineDataList: 個別ラインデータリスト
    """
    # 工場データの準備
    usePow = 0
    costList = {}
    supplyPower = 0

    # 各コスト計算関数を呼び出し
    costList, usePow, supplyPower = _CalculateIndividualLineCosts(iLineDataList, costList, usePow, supplyPower)
    costList = _CalculateStationCost(oLineData, costList)
    costList = _CalculateFloorCost(oLineData, costList)
    costList = _CalculateWallCost(oLineData, costList)

    # 工場データ出力
    factoryData = {}
    factoryData["factoryName"] = oLineData.GetValue(OLineData.FACTORY_NAME_KEY)  # 工場名
    factoryData["usePower"] = usePow  # 消費電力
    factoryData["costList"] = costList
    factoryData["supplyPower"] = supplyPower

    jsonfile = open(pathData.GetPath() + '/' + "FactoryData" + '.json', 'w', encoding='utf-8')
    json.dump(factoryData, jsonfile, indent=4, ensure_ascii=False)
