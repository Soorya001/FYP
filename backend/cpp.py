dataTypesAvailable = {'character':'char', 'boolean':'bool', 'integer':'int', 'float':'float', 'decimal':'decimal','string':'string'}  # Primitive data types only

def for_function(varName,start,end,step):
    startNo = int(start)
    endNo = int(end)
    if(startNo < endNo):
        return f'for({varName}={start};{varName}<={end};{varName}+={step})'
    else:
        return f'for({varName}={start};{varName}>={end};{varName}-={step})'


def headerFile(fileName):
    return f'#include<{fileName}>'

def declaration(varName, dataType, varValue):
    declarationStatement = ""

    if(dataType == "string"):
        declarationStatement = f'{dataType} {varName} = "{varValue}"\n'
    else:
        declarationStatement = f'{dataType} {varName} = {varValue}\n'

    return declarationStatement