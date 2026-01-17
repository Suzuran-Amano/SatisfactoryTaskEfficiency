### 定数 ###

# 配列のキー定数
RESOURCE_NAME_KEY = "resourceName"
PRODUCT_NAME_KEY = "productName"
ITEM_NUM_KEY = "itemNum"


# 資源情報
class ResourceData:

    ### 変数 ###

    # Jsonファイル内のデータ
    jsonData = []

    
    # コンストラクタ
    def __init__(self,data):
        self.jsonData = data
        return
    
    # 値を返す
    def GetValue(self,key : str):
        if key in self.jsonData:
            return self.jsonData[key]
        return None

