from DesignModules import OverallLineEssenceModule as OLineEssence
from DesignModules import OverallLineDataModule as OLineData
from DesignModules import OverallLineDocumentModule as OLineDoc
from DesignModules import IndividualLineEssenceModule as ILineEssence
from DesignModules import pathDataModule


# 全体製造ライン設計書作成用クラス
class OverallLineDesignMaker:

    # constans
    OVERALL_LINE_ESSENCE_NAME = './OverallLineEssence.json'

    # クラス変数

    # 全体ラインデータ
    overallLineEssence = 0
    overallLineData = 0
    
    # 個別ライン本質リスト
    individualLineEssences = 0
    

    def Main(self,pathData : pathDataModule.PathData) -> OLineData:

        # ファイルのフルパスを取得
        inputDataFileName = pathData.GetFullPath()
        if inputDataFileName == "":
            inputDataFileName = self.OVERALL_LINE_ESSENCE_NAME


        # 全体ライン本質を読み込み
        oLineEssence = OLineEssence.OverallLineEssence(inputDataFileName)
        self.overallLineEssence = oLineEssence

        # 全体ラインデータを作成
        overallLineData = OLineData.OverallLineData(oLineEssence)
        overallLineData.Output(pathData.GetPath())

        # 全体ライン書類を出力
        overallLineDocument = OLineDoc.OverallLineDocument()
        overallLineDocument.MakeDocument(pathData,overallLineData)

        # 個別ライン本質リストの作成
        individualLineEssences = self.MakeILineEssence(overallLineData)
        self.individualLineEssences = individualLineEssences
        for iLineEssence in individualLineEssences :
            iLineEssence.Output(pathData.GetPath())


        return overallLineData
    


    # 個別ライン本質ファイルの作成
    def MakeILineEssence(self,oLineData :OLineData) -> list:
        
        result = []

        # 個別ラインの情報を取得
        iLines = oLineData.GetValue(OLineData.INDIVIDUAL_LINE_LIST)

        # 個別ラインの情報から、個別ライン本質を作成し、リストへ加える
        for iLine in iLines:
            lineEssense = {}
            lineEssense[ILineEssence.LINE_NAME_KEY] = iLine[OLineData.INDIVIDUAL_LINE_NAME]
            lineEssense[ILineEssence.RECIPE_NAME_KEY] = iLine[OLineData.RECIPE_NAME_KEY]
            lineEssense[ILineEssence.RECIPE_NUM_KEY] = iLine[OLineData.RECIPE_NUM_KEY]
            result.append(ILineEssence.IndividualLineEssence(lineEssense))

        return result
