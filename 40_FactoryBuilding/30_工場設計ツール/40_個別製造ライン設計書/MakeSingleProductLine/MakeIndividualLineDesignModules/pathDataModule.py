

class PathData:

    argument = {}


    # 初期化
    def __init__(self,argv):
        self.argument = argv

    # ファイル名を返す
    def GetFileName(self) :
        return self.argument[1]
    
    # ファイルパスを返す
    def GetFilePath(self):
        # argment 変数の要素数が2より少なかったら無を返す
        if len(self.argument) < 2:
            return ""
        return self.argument[2]
