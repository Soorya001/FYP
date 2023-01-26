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