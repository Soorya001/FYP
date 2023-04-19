import cpp
import re
import java
import python
import math

forPossibilities = ["iterate", "for", "loop", "traverse", "traverses"]
declarationPossibilities = ["declare", "initialize", "variable"]
outputPossibilities = ["print", "show", "output"]
assignPossibilities = ["assign", "set"]
functionCallPossibilities = ["invoke","call"]
functionCallArgumentPossibilities = ["parameter","parameters","argument","arguments"]


def extract_keywords(str, language, indentation):
    varName=""
    rangeStart=""
    rangeEnd=""
    stepCount=""
    str = str.lower()
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
        elif (language == "java"):
            return ((java.for_function(varName, rangeStart, rangeEnd, stepCount)), indentation)
        
    elif any(phrase in strList for phrase in outputPossibilities):
        res = re.search('print (.*)', str)
        content = res.group(1).strip()

        if (language == "python"):
            return ((python.printStatement(content)), indentation)
        elif (language == "cpp"):
            return ((cpp.printStatement(content)), indentation)
        elif (language == "java"):
            return ((java.printStatement(content)), indentation)
        

    # assign variable a value 10
    elif any(phrase in strList for phrase in assignPossibilities):

        res = re.search('variable (.*) value', str)
        varName = res.group(1).strip()

        res = re.search('value (.*)', str)
        varValue = res.group(1).strip()

        if (language == "python"):
            return (f"{varName} = {varValue}\n", indentation)
        elif (language == "cpp"):
            return (f"{varName} = {varValue};\n", indentation)
        



    elif ("include" in str) or ("Include" in str):              # Header Files
        res = re.search('file (.*)', str)

        if (res == None or len(res) <= 1) and language == "cpp":
            return (("#include<iostream>\n#include<string.h>\nusing namespace std;\n"), indentation)

        else:
            fileName = res.group(1).strip()
            if (language == "python"):
                return ((python.headerFile(fileName)), indentation)
            elif (language == "cpp"):
                return ((cpp.headerFile(fileName)), indentation)

    # Open and close Brackets - { } - Blocks
    elif ("block" in str) or ("Block" in str):
        if language == "cpp" or language == "java":
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
    elif any(phrase in strList for phrase in declarationPossibilities):
        varValue = ""
        dataType = ""
        

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
        elif (language == "java"):
            return ((java.declaration(varName, dataType, varValue)), indentation)

    elif ("main" in str):
        functionName = "main"
        returnType = "integer"
        arguments = []

        if (language == "cpp"):
            return (cpp.createFunction(functionName, returnType, arguments), indentation)
        elif (language == "python"):
            return (python.createFunction(functionName, returnType, arguments), indentation)
        elif (language == "java"):
            return ("public static void main(String[] args)", indentation)

    elif any(phrase in strList for phrase in functionCallPossibilities):
        functionName = ""
        functionNameIndex = -1
        parametersIndex = -1
        arguments = []

        try:
            functionNameIndex = strList.index("function")
        except Exception as e:
            return ("",indentation)
        
        if( ( functionNameIndex + 1 ) < len(strList) ):
            functionName = strList[ functionNameIndex + 1 ]

        for functionCallArgumentPossibility in functionCallArgumentPossibilities:
            if functionCallArgumentPossibility in strList:
                parametersIndex = strList.index(functionCallArgumentPossibility)
                break

        if parametersIndex == -1:
            if (language == "cpp"):
                return (cpp.functionCall(functionName,arguments), indentation)
            elif (language == "python"):
                return (python.functionCall(functionName,arguments), indentation)
            elif (language == "java"):
                return (java.functionCall(functionName,arguments), indentation)
            
        else:
            res = re.search(f'{strList[parametersIndex]} (.*)',str)
            argumentGroup = res.group(1).strip()

            arguments = argumentGroup.split("and")
            arguments = [e.strip() for e in arguments]
            print("Funciton name : ",functionName)
            print("Arguments are : ",arguments)
            if (language == "cpp"):
                return (cpp.functionCall(functionName,arguments), indentation)
            elif (language == "python"):
                return (python.functionCall(functionName,arguments), indentation)
            
    elif ( ("function" in str) or ("Function" in str)):
        functionNameIndex = strList.index("function")
        returnTypeIndex = strList.index("type")
        parametersIndex = strList.index("parameters")

        if( ( functionNameIndex + 1 ) < len(strList) ):
            functionName = strList[ functionNameIndex + 1 ]
        else:
            functionName = ""
        
        if( ( returnTypeIndex + 1 ) < len(strList)):
            returnType = strList[ returnTypeIndex + 1 ]
        else:
            returnType = ""
        
        res = re.search('parameters (.*)',str)
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
        elif (language == "java"):
            return (java.createFunction(functionName, returnType, arguments), indentation)
        
    
    elif "class" in strList:
        classNameIndex = strList.index("class")
        className = "undefined"
        if(classNameIndex + 1 < len(strList)):
            className = strList[classNameIndex + 1]
        # print("Class NAME iS : ", className)
        return (java.create_class(className), indentation)

    else:                           # For testing purposes. I can give print statments to see the output. Should remove later
        return (str+"\n", indentation)
    
