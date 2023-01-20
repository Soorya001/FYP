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

def declaration(varName, userDataType, varValue):
    dataType=""
    if(userDataType in dataTypesAvailable):
        dataType = dataTypesAvailable[userDataType]
    # else:                                            Should implement the case when none of the primitive data types match with userDataType
    #     dataType="void"

    declarationStatement = ""

    if(dataType=="string"):
        declarationStatement = f"{dataType} {varName} = \"{varValue}\";\n"
    else:
        declarationStatement = f"{dataType} {varName} = {varValue};\n"

    return declarationStatement