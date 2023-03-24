import re

dataTypesAvailable = {'character': 'char', 'boolean': 'bool', 'integer': 'int', 'float': 'float',
                      'decimal': 'decimal', 'string': 'string', 'void': 'void'}  # Primitive data types only


def for_function(varName, start, end, step):
    startNo = int(start)
    endNo = int(end)
    if (startNo < endNo):
        return f'for({varName}={start};{varName}<={end};{varName}+={step})\n'
    else:
        return f'for({varName}={start};{varName}>={end};{varName}-={step})\n'


def headerFile(fileName):
    return f'#include<{fileName}>\n'


def declaration(varName, dataType, varValue):
    declarationStatement = ""

    if (dataType == "string"):
        declarationStatement = f'{dataTypesAvailable[dataType]} {varName} = "{varValue}";\n'
    else:
        declarationStatement = f'{dataTypesAvailable[dataType]} {varName} = {varValue};\n'

    return declarationStatement


def createFunction(functionName, returnType, arguments):

    returnType = dataTypesAvailable[returnType]

    for argument in arguments:
        argument[0] = dataTypesAvailable[argument[0]]+" "

    argumentsString = ""
    for argument in arguments:
        argumentsString = argumentsString + " , " + "".join(argument)

    if (len(argumentsString) > 2):
        argumentsString = argumentsString[3:]


    return f"{returnType} {functionName}({argumentsString})\n"


def printStatement(content):
    if "string" in content:
        res = re.search('string (.*)', content)
        content = res.group(1).strip()
        content = f' "{content} " '
    
    return f"cout<<({content});\n"

def functionCall(functionName, parameters):
    if parameters == "":
        return f"{functionName}();\n"
    else:
        s = ",".join(parameters)
        return f"{functionName}(" + s + ");\n"
    

