import inspector
import pyperclip
import sys

# Load file from argument or fall back to a default
if len(sys.argv) > 1:
    filepath = sys.argv[1]
    with open(filepath, "r") as f:
        currentFile = f.read().replace("\n","")
else:
    filepath = None
    currentFile = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Renzo Project</title>
</head>
<body>
    <h1>Hello World!</h1>
</body>
</html>'''
if len(currentFile)== 0:
    currentFile = "<!DOCTYPE html><html><head></head><body></body></html>"

debug = ""

def save():
    global debug
    if filepath:
        with open(filepath, "w") as f:
            f.write(currentFile)
        debug = f"Saved to {filepath}"
    else:
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

class FakeNode:
    """A lightweight node-like object used only for stack tracking."""
    def __init__(self, name, indent):
        self.name = name
        self.indent = indent

def convertToString(tags):
    res = ""
    tagStack = []
    prev_indent = None

    for i in tags:
        while tagStack and tagStack[-1].indent >= i.indent:
            closed = tagStack.pop()
            if hasEnd(closed.name) and not isinstance(closed, inspector.inner):
                res += "    " * closed.indent + "</" + closed.name + ">\n"

        if prev_indent is not None and i.indent > prev_indent:
            res += "\n"

        if isinstance(i, inspector.inner):
            res += "    " * i.indent + i.name + "\n"
        else:
            res += "    " * i.indent + "<" + i.name + propertiesToString(i.properties) + ">"
            if hasEnd(i.name):
                tagStack.append(i)
            else:
                res += "\n"

        prev_indent = i.indent

    # Close any tags still open at the end
    while tagStack:
        closed = tagStack.pop()
        if hasEnd(closed.name) and not isinstance(closed, inspector.inner):
            res += "    " * closed.indent + "</" + closed.name + ">\n"
    global currentFile
    currentFile = res
    return res

def hasEnd(tag):
    if tag.startswith("!DOCTYPE") or tag.startswith("meta"):
        return False
    return True


def getRaw():
    return currentFile.replace("\n", "")