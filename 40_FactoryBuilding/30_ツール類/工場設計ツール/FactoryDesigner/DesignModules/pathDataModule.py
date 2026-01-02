import os

OVERALL_LINE_DIRECTORY_NAME = "30_全体製造ライン設計書"
INDIVIDUAL_LINE_DIRECTORY_NAME = "40_個別製造ライン設計書"
INDIVIDUAL_TEST_DIRECTORY_NAME = "60_個別製造ラインテスト項目書"

class PathData:

    # 変数
    argument = {}


    # 初期化
    def __init__(self,argv):
        self.argument = argv

    # ファイル名を返す
    def GetFullPath(self) :
        return self.argument[1]
    
    # ファイルパスを返す
    def GetPath(self):
        # argment 変数の要素数が2より少なかったら無を返す
        if len(self.argument) < 2:
            return ""
        return self.argument[2]
    
    def GetFileName(self):
        return os.path.basename(self.argument[1])
    
    # デバッグ用に表示する
    def Print(self):
        print(self.GetFullPath())
        print(self.GetPath())
        print(self.GetFileName())
