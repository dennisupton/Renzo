import inspector
import pyperclip

# Load file from argument or fall back to a default
if len(sys.argv) > 1:
    filepath = sys.argv[1]
    with open(filepath, "r") as f:
        currentFile = f.read()
else:
    filepath = None
    currentFile = "<!DOCTYPE html><html><head></head><body></body></html>"


debug = ""

def save():
    global debug
    pyperclip.copy(currentFile)
    debug = "Saved to clipboard"

def propertiesToString(properties):
    res = ""
    for key,value in properties.items():
        if type(value) == str:
            res += " "+key+'="'+value+'"'
        elif type(value) == bool and value:
            res += " "+key
    return res
def convertToString(tags):
    global currentFile
    res = ""
    lasttag = None
    tagStack = []
    for i in tags:
        if lasttag and i.indent <= lasttag.indent:
            skipped = 0
            if hasEnd(lasttag.name) and not isinstance(lasttag, inspector.inner):
                res += "    "*lasttag.indent+"</"+lasttag.name+">"
                res += "\n"
                tagStack.remove(lasttag)

            for indent in range(lasttag.indent-i.indent):
                if hasEnd(tagStack[-1].name) and not isinstance(tagStack[-1], inspector.inner):
                    res += "    "*tagStack[-1].indent+"</"+tagStack[-1].name+">"
                    res += "\n"
                if isinstance(tagStack[-1], inspector.inner) or not hasEnd(tagStack[-1].name):
                    skipped += 1
                tagStack.pop(-1)
            while skipped > 0 and len(tagStack)>0:
                if hasEnd(tagStack[-1].name) and not isinstance(tagStack[-1], inspector.inner):
                    res += "    "*tagStack[-1].indent+"</"+tagStack[-1].name+">"
                    res += "\n"
                if isinstance(tagStack[-1], inspector.inner) or not hasEnd(tagStack[-1].name):
                    skipped += 1
                tagStack.pop(-1)
                skipped -= 1
        elif lasttag and i.indent > lasttag.indent:
            res += "\n"


        if isinstance(i, inspector.inner):
            res += "    "*i.indent+i.name
            res += "\n"

        else:
            res += "    "*i.indent+"<"+i.name+ propertiesToString(i.properties)+">"
        if not hasEnd(i.name):
            res += "\n"
        
        tagStack.append(i)
        lasttag = i
    skipped = 0
    while len(tagStack)>0:
        if hasEnd(tagStack[-1].name) and not isinstance(tagStack[-1], inspector.inner):
            res += "    "*tagStack[-1].indent+"</"+tagStack[-1].name+">"
            res += "\n"
        if isinstance(tagStack[-1], inspector.inner):
            skipped += 1
        tagStack.pop(-1)
    while skipped > 0 and len(tagStack)>0:
        if hasEnd(tagStack[-1].name) and not isinstance(tagStack[-1], inspector.inner):
            res += "    "*tagStack[-1].indent+"</"+tagStack[-1].name+">"
            res += "\n"
        if isinstance(tagStack[-1], inspector.inner) or not hasEnd(tagStack[-1].name):
            skipped += 1
        tagStack.pop(-1)
        skipped -= 1

    currentFile = res

def hasEnd(tag):
    if tag.startswith("!DOCTYPE") or tag.startswith("meta"):
        return False
    return True


def getRaw():
    return currentFile.replace("\n", "")