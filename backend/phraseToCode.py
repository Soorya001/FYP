import cpp
import re
import python

def extract_keywords(str,language):
    varName=""
    rangeStart=""
    rangeEnd=""
    stepCount=""

    if ("iterate" in str) or ("Iterate" in str):

        res = re.search('iterate'+'(.*)'+'from',str)
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


    elif ("for" in str) or ("For" in str):
    
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

    elif ("include" in str) or ("Include" in str):              # Header Files
        res = re.search('file (.*)', str)
        fileName = res.group(1).strip()

        if(language == "python"):
            return (python.headerFile(fileName))
        elif(language == "cpp"):
            return (cpp.headerFile(fileName))

    elif ("block" in str ) or ("Block" in str):                 # Open and close Brackets - { } - Blocks
        if language == "cpp":
            if ("open" in str) or ("Open" in str):
                return "{\n"
            elif ("close" in str) or ("Close" in str):
                return "}\n"

        elif language == "python":
            if ("open" in str) or ("Open" in str):
                return "\n\t"
            elif ("close" in str) or ("Close" in str):
                return "\n\b\b\b\b"


    elif ("bracket" in str) or ("Bracket" in str):         # Open and close Backets - ( )
        if ("open" in str) or ("Open" in str):
            return "("
        elif ("close" in str) or ("Close" in str):
            return ")"

    elif ("declare" in str) or ("Declare" in str):              # Declaration Statements
        varValue=""
        dataType=""
        str = str.lower()

        res = re.search('declare' + '(.*)' + 'variable',str)
        dataType = res.group(1).strip()

        res = re.search('variable' + '(.*)' + 'value',str)
        varName = res.group(1).strip()

        res = re.search('value (.*)',str)
        varValue = res.group(1).strip()

        print(varValue)

        if( language == "python"):
            return (python.declaration(varName, dataType, varValue))
        elif (language == "cpp"):
            return (cpp.declaration(varName, dataType, varValue))
