import os
from abc import ABC, abstractmethod

from . import pathDataModule
from . import InfomationReaderModule as InfoReader
from . import RecipeItemModule


# 書類を作成、出力するクラスの基底クラス
class DocumentMaker(ABC):

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