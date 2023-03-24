import re

def for_function(varName, start, end, step):
    startNo = int(start)
    endNo = int(end)
    stepNo = int(step)
    if startNo < endNo:
        return f'for {varName} in range({startNo},{endNo},{stepNo}):\n'
    else:
        return f'for {varName} in range({startNo},{endNo},{-stepNo}):\n'


def headerFile(fileName):
    return f'import {fileName}\n'


def declaration(varName, dataType, varValue):
    declarationStatement = ""

    # Because input varValue will be in lowercase. And boolean value in python are True and False;
    if (dataType == "boolean"):
        varValue = varValue.capitalize()

    if (dataType == "string"):
        declarationStatement = f'{varName} = "{varValue}"\n'
    else:
        declarationStatement = f'{varName} = {varValue}\n'

    return declarationStatement


def createFunction(functionName, returnType, arguments):

    if (len(arguments) == 0):
        argumentsString = ""
    else:
        argumentsList = []
        for argument in arguments:
            argumentsList.append(argument[1])
        print("ArgumentList is:", argumentsList)

        argumentsString = " , ".join(argumentsList)
        # print("argument string is:"+argumentsString)

    return f"def {functionName}( {argumentsString}):\n"


def printStatement(content):
    if "string" in content:
        res = re.search('string (.*)', content)
        content = res.group(1).strip()
        content = f' "{content} "'
    return f"print({content})\n"

def functionCall(functionName, parameters):
    if parameters == "":
        return f"{functionName}()\n"
    else:
        s = ",".join(parameters)
        return f"{functionName}(" + s + ")\n"