import os
from abc import ABC, abstractmethod

from . import pathDataModule
from .BasicData import BasicDataReader
from .BasicData import RecipeData


# 書類を作成、出力するクラスの基底クラス
class DocumentMaker(ABC):
    ### 定数 ###
    REPLACE_KEY_HEADER = "var_"

    # 書類の作成と出力を行う関数
    @abstractmethod
    def MakeDocument(
            self,
            pathData : pathDataModule.PathData,
            oLineData : dict):

        return 
    
    
    # テンプレートファイルを読み込み
    def _ReadTemplateFile(self,templateFileName) -> list:
        lines = []
        abs_path = os.path.abspath(__file__)
        dir_path = os.path.dirname(abs_path)
        filePath = dir_path + "\\" + templateFileName
        with open(filePath, encoding="utf-8") as f:
            for line in f:
                lines.append(line.rstrip())
        return lines


    # 書類データを保存
    def _WriteFile(
            self,
            path : str,
            fileName : str,
            lines : list
            ):

        os.makedirs(path, exist_ok=True)
        with open(path + "\\" + fileName , "w", encoding="utf-8") as o:
            for line in lines:
                print(line,file=o)
        return
    

    # 置き換えキーを取得
    def _GetReplaceKey(self,key):
        return self.REPLACE_KEY_HEADER + key


    # 置き換え
    def _AllLineReplace(
            self,
            lines : list,
            data : dict
            ) -> list:

        for index in range(len(lines)):
            lines[index] = self._Replace(lines[index],data)

        return lines


    # 置き換え
    def _Replace(
            self,
            text : str,
            data : dict
            ) -> str:
                
        for key,value in data.items():
            if key in text:
                text = text.replace(self._GetReplaceKey(key),str(value))
        return text
    
    
    # 物品の数分を複製する
    def _DuplicateLines(
            self,
            lines,
            length : int,
            keys : list
            ):
        
        resultLines = []

        # 複製
        for line in lines:
            
            # 複製する必要があるかを判定
            shouldReplace = False
            for key in keys:
                if key in line:
                    shouldReplace = True
                    break
            
            # 複製する必要が無かったら
            if not(shouldReplace):
                resultLines.append(line)
                continue


            # 複製する必要があるなら
            for f in range(length):
                newLine = line
                for key in keys:
                    newLine = newLine.replace(key, key + str(f+1))
                resultLines.append(newLine)

        return resultLines