
def hasEnd(node):
    if node.startswith("!DOCTYPE") or node.startswith("html") or node.startswith("meta"):
        return False
    return True

class inspectorPanel:
    def __init__(self):
        self.nodes = []
        self.selectedNode = 0

    def up(self):
        self.selectedNode -= 1
        if self.selectedNode < 0:
            self.selectedNode = 0
        
    
    def down(self):
        self.selectedNode += 1
        if self.selectedNode > len(self.nodes)-1:
            self.selectedNode = len(self.nodes)-1

    def parse(self,html):
        self.nodes = []
        indent = 0
        newNodeName = False
        nodeName = ""
        nodeProperties = ""
        for i in html:
            if i == "<":
                newNodeName = True
            elif newNodeName and i == "/":
                newNodeName = False
                indent -= 1
            elif i =="/":
                indent -= 1
            elif newNodeName and i == ">":
                self.nodes.append(node(nodeName, indent))
                if hasEnd(nodeName):
                    indent += 1
                nodeName = ""
                newNodeName = False
            elif newNodeName:
                nodeName += i
    
class node:
    def __init__(self, name, indent):
        self.name = name.split(" ", -1)[0]
        self.indent = indent
        self.parseProperties(name.split(" ", -1)[1:])
    
    def parseProperties(self,rawList):
        self.properties = {}
        for i in rawList:
            raw = i.split("=",-1)
            if len(raw) > 1:
                self.properties[raw[0]] = raw[1]