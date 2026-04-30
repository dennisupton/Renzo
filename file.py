import inspector
import pyperclip


currentFile='''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <h1>hello!</h1>
    <div><div>hello</div></div>
</body>
</html>
'''

debug = ""

def save():
    pyperclip.copy("currentFile")

def propertiesToString(properties):
    res = ""
    for key,value in properties.items():
        if type(value) == str:
            res += " "+key+'="'+value+'"'
        elif type(value) == bool and value:
            res += " "+key
    return res
def convertToString(nodes):
    global currentFile
    res = ""
    lastNode = None
    nodeStack = []
    for i in nodes:
        if lastNode and i.indent <= lastNode.indent:
            skipped = 0
            if hasEnd(lastNode.name) and not isinstance(lastNode, inspector.inner):
                res += "    "*lastNode.indent+"</"+lastNode.name+">"
                res += "\n"
                nodeStack.remove(lastNode)

            for indent in range(lastNode.indent-i.indent):
                if hasEnd(nodeStack[-1].name) and not isinstance(nodeStack[-1], inspector.inner):
                    res += "    "*nodeStack[-1].indent+"</"+nodeStack[-1].name+">"
                    res += "\n"
                if isinstance(nodeStack[-1], inspector.inner) or not hasEnd(nodeStack[-1].name):
                    skipped += 1
                nodeStack.pop(-1)
            while skipped > 0 and len(nodeStack)>0:
                if hasEnd(nodeStack[-1].name) and not isinstance(nodeStack[-1], inspector.inner):
                    res += "    "*nodeStack[-1].indent+"</"+nodeStack[-1].name+">"
                    res += "\n"
                if isinstance(nodeStack[-1], inspector.inner) or not hasEnd(nodeStack[-1].name):
                    skipped += 1
                nodeStack.pop(-1)
                skipped -= 1
        elif lastNode and i.indent > lastNode.indent:
            res += "\n"


        if isinstance(i, inspector.inner):
            res += "    "*i.indent+i.name
            res += "\n"

        else:
            res += "    "*i.indent+"<"+i.name+ propertiesToString(i.properties)+">"
        if not hasEnd(i.name):
            res += "\n"
        
        nodeStack.append(i)
        lastNode = i
    skipped = 0
    while len(nodeStack)>0:
        if hasEnd(nodeStack[-1].name) and not isinstance(nodeStack[-1], inspector.inner):
            res += "    "*nodeStack[-1].indent+"</"+nodeStack[-1].name+">"
            res += "\n"
        if isinstance(nodeStack[-1], inspector.inner):
            skipped += 1
        nodeStack.pop(-1)
    while skipped > 0 and len(nodeStack)>0:
        if hasEnd(nodeStack[-1].name) and not isinstance(nodeStack[-1], inspector.inner):
            res += "    "*nodeStack[-1].indent+"</"+nodeStack[-1].name+">"
            res += "\n"
        if isinstance(nodeStack[-1], inspector.inner) or not hasEnd(nodeStack[-1].name):
            skipped += 1
        nodeStack.pop(-1)
        skipped -= 1

    currentFile = res

def hasEnd(node):
    if node.startswith("!DOCTYPE") or node.startswith("meta"):
        return False
    return True


def getRaw():
    return currentFile.replace("\n", "")