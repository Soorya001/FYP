import cpp
import re
import python

def extract_keywords(str,language):
    varName=""
    rangeStart=""
    rangeEnd=""
    stepCount=""
    if ("for" in str) or ("For" in str):
    
        res = re.search('loop'+'(.*)'+'from',str)
        varName = res.group(1).strip()

        res = re.search('from'+'(.*)'+'till',str)
        rangeStart = res.group(1).strip()

        res = re.search('till' + '(.*)' + 'step', str)
        rangeEnd = res.group(1).strip()

        res = re.search('count (.*)', str)
        stepCount = res.group(1).strip()

        if(language == "python"):
            return (python.for_function(varName,rangeStart,rangeEnd,stepCount))
        elif(language == "cpp"):
            return (cpp.for_function(varName,rangeStart,rangeEnd,stepCount))

