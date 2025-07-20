import os
import json

import recipeManager


class IndividualLineDesignMaker:

    # constans
    inputTextFileName = './個別製造ライン設計書_var_outputName製造ライン.md'
    inputDataFileName = './IndividualLine.json'
    outputFileName = './個別製造ライン設計書_var_outputName製造ライン.md'


    data=[]

    inputNum = 0
    outputNum = 0


    def Replace(self,text):

        for dat in self.data:
            text = text.replace("var_" + dat[0],dat[1])

        return text


    def GetVarByKey(self,key):
        result = ""
        for dat in self.data:
            if dat[0] == key:
                result = dat[1]
        return result


    def MakeFlowChart(self,):

        result = []

        inputName = str(self.GetVarByKey("inputName"))
        outputName = str(self.GetVarByKey("outputName"))
        productName = str(self.GetVarByKey("productName"))
        productNum = int(self.GetVarByKey("recipeNum"))
            
        # header
        result.append("```mermaid")
        result.append("flowchart TD\n")

        # input
        result.append("subgraph Input")
        result.append("    " + inputName +"([" + inputName + "])")
        result.append("end\n")

        # product
        for i in range(productNum):

            result.append(productName + str(i+1) + "[")
            result.append("    " + productName + str(i+1))
            result.append("    " + inputName + " " + str(self.inputNum) + "/m")
            result.append("    ↓")
            result.append("    " + outputName + " " + str(self.outputNum) + "/m" )
            result.append("]\n")

        # output
        result.append("subgraph Output")
        result.append("    " + outputName +"([" + outputName + "])")
        result.append("end\n")


        for i in range(productNum):

            result.append(inputName + "-->|" + str(self.inputNum) + "|" + productName + str(i+1))
            result.append(productName + str(i+1) + "-->|" + str(self.outputNum) + "|" + outputName)

        result.append("```\n")
        
        return result


    def Main(self):
        lines = []

        # input file read
        os.chdir(os.path.dirname(__file__) + "/../")
        with open(self.inputTextFileName, encoding="utf-8") as f:
            for line in f:
                lines.append(line.rstrip())


        # input data
        os.chdir(os.path.dirname(__file__) + "/../")
        lineData = json.load(open('./IndividualLine.json','r', encoding="utf-8"))
        recipes = recipeManager.RecipeReader()
        recipe = recipes.GetRecipe(lineData["recipeName"])


        # Calc TotalOutput,TotalInput
        inputNum = recipe.GetInputItemList()[0]["itemNum"]
        self.data.append(["inputNum",str(inputNum)])
        outputNum = recipe.GetOutputItemList()[0]["itemNum"]
        self.data.append(["outputNum",str(outputNum)])
        productNum = lineData["recipeNum"]
        self.data.append(["recipeNum",str(productNum)])
        self.data.append(["totalInput",str(productNum*inputNum)])
        self.data.append(["totalOutput",str(productNum*outputNum)])

        inputName = recipe.GetInputItemList()[0]["itemName"]
        self.data.append(["inputName",str(inputName)])

        outputName = recipe.GetOutputItemList()[0]["itemName"]
        self.data.append(["outputName",str(outputName)])

        self.data.append(["productName",recipe.GetProductName()])


        # MakeFlowChart
        insertNum = 0
        for index, item in enumerate(lines):
            if item == "## 製造ライン":
                insertNum = index + 1

        flowChart = self.MakeFlowChart()

        for chartLine in flowChart:
            lines.insert(insertNum,chartLine)
            insertNum += 1


        # replace
        for index, item in enumerate(lines):
            lines[index] = self.Replace(lines[index])


        # text output
        os.chdir(os.path.dirname(__file__) + "/../")
        fileName = self.Replace(self.outputFileName)
        with open(fileName,"w", encoding="utf-8") as o:
            for line in lines:
                print(line,file=o)


