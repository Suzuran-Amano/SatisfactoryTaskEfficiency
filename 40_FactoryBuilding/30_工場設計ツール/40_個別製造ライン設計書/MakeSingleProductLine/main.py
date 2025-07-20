import os
import json

import recipeManager

# constans
inputTextFileName = './個別製造ライン設計書_var_outputName製造ライン.md'
inputDataFileName = './Seed.csv'
outputFileName = './個別製造ライン設計書_var_outputName製造ライン.md'



lines=[]
data=[]



def Replace(text):

    for dat in data:
        text = text.replace("var_" + dat[0],dat[1])

    return text


def GetVarByKey(key):
    result = ""
    for dat in data:
        if dat[0] == key:
            result = dat[1]
    return result


def MakeFlowChart():

    result = []

    inputName = str(GetVarByKey("inputName"))
    outputName = str(GetVarByKey("outputName"))
    productName = str(GetVarByKey("productName"))
    productNum = int(GetVarByKey("recipeNum"))
        
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
        result.append("    " + inputName + " " + str(inputNum) + "/m")
        result.append("    ↓")
        result.append("    " + outputName + " " + str(outputNum) + "/m" )
        result.append("]\n")

    # output
    result.append("subgraph Output")
    result.append("    " + outputName +"([" + outputName + "])")
    result.append("end\n")


    for i in range(productNum):

        result.append(inputName + "-->|" + str(inputNum) + "|" + productName + str(i+1))
        result.append(productName + str(i+1) + "-->|" + str(outputNum) + "|" + outputName)

    result.append("```\n")
    
    return result



# input file read
os.chdir(os.path.dirname(__file__) + "/../")
with open(inputTextFileName, encoding="utf-8") as f:
    for line in f:
       lines.append(line.rstrip())


# input data
os.chdir(os.path.dirname(__file__) + "/../")
lineData = json.load(open('./IndividualLine.json','r', encoding="utf-8"))
recipes = recipeManager.RecipeReader()
recipe = recipes.GetRecipe(lineData["recipeName"])

# Calc TotalOutput,TotalInput
inputNum = recipe.GetInputItemList()[0]["itemNum"]
data.append(["inputNum",str(inputNum)])
outputNum = recipe.GetOutputItemList()[0]["itemNum"]
data.append(["outputNum",str(outputNum)])
productNum = lineData["recipeNum"]
data.append(["recipeNum",str(productNum)])
data.append(["totalInput",str(productNum*inputNum)])
data.append(["totalOutput",str(productNum*outputNum)])

inputName = recipe.GetInputItemList()[0]["itemName"]
data.append(["inputName",str(inputName)])

outputName = recipe.GetOutputItemList()[0]["itemName"]
data.append(["outputName",str(outputName)])

data.append(["productName",recipe.GetProductName()])


# MakeFlowChart
insertNum = 0
for index, item in enumerate(lines):
    if item == "## 製造ライン":
        insertNum = index + 1

flowChart = MakeFlowChart()

for chartLine in flowChart:
    lines.insert(insertNum,chartLine)
    insertNum += 1


# replace
for index, item in enumerate(lines):
    lines[index] = Replace(lines[index])


# text output
os.chdir(os.path.dirname(__file__) + "/../")
fileName = Replace(outputFileName)
with open(fileName,"w", encoding="utf-8") as o:
    for line in lines:
        print(line,file=o)


