def for_function(varName,start,end,step):
    startNo = int(start)
    endNo = int(end)
    stepNo = int(step)
    if startNo < endNo:
        return f'for {varName} in range({startNo},{endNo},{stepNo}):'
    else:
        return f'for {varName} in range({startNo},{endNo},{-stepNo}):'


def headerFile(fileName):
    return f'import {fileName}\n'

def declaration(varName, dataType, varValue):
    declarationStatement = ""

    if(dataType == "boolean"):                          # Because input varValue will be in lowercase. And boolean value in python are True and False;
        varValue = varValue.capitalize()

    if(dataType == "string"):
        declarationStatement = f'{varName} = "{varValue}"\n'
    else:
        declarationStatement = f'{varName} = {varValue}\n'

    return declarationStatement
