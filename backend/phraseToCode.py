import cpp
import re
import python
import math

forPossibilities = ["iterate", "for", "loop", "traverse", "traverses"]
declarationPossibilites = ["declare", "initialize", "variable"]


def extract_keywords(str, language, indentation):
    varName = ""
    rangeStart = ""
    rangeEnd = ""
    stepCount = ""

    # Splits the string into list of individual word
    strList = str.split()

    if any(phrase in strList for phrase in forPossibilities):

        # Word followed by 'variable' is the variable name

        if "variable" in strList:
            ind = strList.index("variable")
            if ind < (len(strList) - 1):
                varName = strList[ind+1]

        # extracts all numbers in the string str
        numValues = [int(s) for s in re.findall(r'-?\d+\.?\d*', str)]

        print("Num values are: ", numValues)
        if (len(numValues) >= 3):
            rangeStart = numValues[0]
            rangeEnd = numValues[1]
            stepCount = numValues[2]

        if (language == "python"):
            return ((python.for_function(varName, rangeStart, rangeEnd, stepCount)), indentation)
        elif (language == "cpp"):
            return ((cpp.for_function(varName, rangeStart, rangeEnd, stepCount)), indentation)

    elif ("include" in str) or ("Include" in str):              # Header Files
        res = re.search('file (.*)', str)
        fileName = res.group(1).strip()

        if (language == "python"):
            return ((python.headerFile(fileName)), indentation)
        elif (language == "cpp"):
            return ((cpp.headerFile(fileName)), indentation)

    # Open and close Brackets - { } - Blocks
    elif ("block" in str) or ("Block" in str):
        if language == "cpp":
            if ("open" in str) or ("Open" in str):
                return ("{\n", indentation)

            elif ("close" in str) or ("Close" in str):
                indentation -= 1
                indentation = max(0, indentation)
                return ("}\n", indentation)

        elif language == "python":
            if ("open" in str) or ("Open" in str):
                indentation += 1
                return ("\n", indentation)
            elif ("close" in str) or ("Close" in str):
                indentation -= 1
                indentation = max(0, indentation)
                return ("\n", indentation)

    elif ("bracket" in str) or ("Bracket" in str):         # Open and close Backets - ( )
        if ("open" in str) or ("Open" in str):
            return ("(", indentation)
        elif ("close" in str) or ("Close" in str):
            return (")", indentation)

    # Declaration Statements
    elif any(phrase in strList for phrase in declarationPossibilites):
        varValue = ""
        dataType = ""
        str = str.lower()

        # Format - "{any of the declarationPossibilities}... {dataType} variable {variableName}.... {value}"
        varNameIndex = strList.index("variable")
        varValueIndex = strList.index("value")
        if (varNameIndex+1) < len(strList) and (varNameIndex-1) >= 0:
            varName = strList[varNameIndex + 1]
            dataType = strList[varNameIndex - 1]

        if (varValueIndex + 1) < len(strList):
            varValue = strList[varValueIndex + 1]

        print(varValue)

        if (language == "python"):
            return ((python.declaration(varName, dataType, varValue)), indentation)
        elif (language == "cpp"):
            return ((cpp.declaration(varName, dataType, varValue)), indentation)

    elif ("main" in str):
        functionName = "main"
        returnType = "integer"
        arguments = []

        if (language == "cpp"):
            return (cpp.createFunction(functionName, returnType, arguments), indentation)
        elif (language == "python"):
            return (python.createFunction(functionName, returnType, arguments), indentation)

    elif (("function" in str) or ("Function" in str)):
        res = re.search('function' + '(.*)' + 'type', str)
        functionName = res.group(1).strip()

        res = re.search('type' + '(.*)' + 'parameters', str)
        returnType = res.group(1).strip()

        res = re.search('parameters (.*)', str)
        argumentGroup = res.group(1).strip()

        # print("Function name:"+functionName+"Return Type:"+returnType+"PArameters:"+arguments)
        # ['integer i', 'float j']

        if (not (argumentGroup == "none" or argumentGroup == "None")):
            indarg = argumentGroup.split("and")
            indarg = [e.strip() for e in indarg]
            arguments = []
            for arg in indarg:
                individualArgument = [dataType, varName] = arg.split(' ')
                arguments.append(individualArgument)
        else:
            arguments = []

        # print("Arguments are: ",arguments)
        if (language == "cpp"):
            return (cpp.createFunction(functionName, returnType, arguments), indentation)
        elif (language == "python"):
            return (python.createFunction(functionName, returnType, arguments), indentation)

    else:                           # For testing purposes. I can give print statments to see the output. Should remove later
        return (str+"\n", indentation)
