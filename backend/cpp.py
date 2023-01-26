def for_function(varName,start,end,step):
    startNo = int(start)
    endNo = int(end)
    if(startNo < endNo):
        return f'for({varName}={start};{varName}<={end};{varName}+={step})'
    else:
        return f'for({varName}={start};{varName}>={end};{varName}-={step})'


def headerFile(fileName):
    return f'#include<{fileName}>\n'