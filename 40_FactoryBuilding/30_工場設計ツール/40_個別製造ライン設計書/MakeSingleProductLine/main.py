import sys

import MakeIndividualLineDesign
import MakeIndividualLineCheckList



designMaker = MakeIndividualLineDesign.IndividualLineDesignMaker()
designMaker.Main(sys.argv)

checkListMaker = MakeIndividualLineCheckList.MakeIndividualLineCheckList()
checkListMaker.Main(sys.argv)