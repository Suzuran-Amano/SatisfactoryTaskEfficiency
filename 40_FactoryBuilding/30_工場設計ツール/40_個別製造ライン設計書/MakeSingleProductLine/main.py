import sys

import MakeIndividualLineDesign
import MakeIndividualLineCheckList


# 個別製造ライン設計書作成
designMaker = MakeIndividualLineDesign.IndividualLineDesignMaker()
designMaker.Main(sys.argv)

# 個別製造ラインテスト項目書作成
checkListMaker = MakeIndividualLineCheckList.MakeIndividualLineCheckList()
checkListMaker.Main(sys.argv)