import re



def hasEnd(node):
    if node.startswith("!DOCTYPE") or node.startswith("html") or node.startswith("meta"):
        return False
    return True

class inspectorPanel:
    def __init__(self):
        self.nodes = []
        self.selectedNode = 0

    def getIndentList(self):
        res = []
        for i in self.nodes:
            res.append(i.indent)
        return res

    def up(self):
        self.selectedNode -= 1
        if self.selectedNode < 0:
            self.selectedNode = 0
    
    def down(self):
        self.selectedNode += 1
        if self.selectedNode > len(self.nodes)-1:
            self.selectedNode = len(self.nodes)-1

    def enter(self):
        global panel, propertyEditor
        panel = propertyEditor

    def parse(self,html):
        self.nodes = []
        indent = 0
        newNodeName = False
        nodeName = ""
        nodeProperties = ""
        innerText = ""
        inNode = False
        global inner
        for i in html:
            if newNodeName and i == "/":
                newNodeName = False
                indent -= 1
            elif i =="/":
                indent -= 1
            elif newNodeName and i == ">":
                inNode = False
                self.nodes.append(node(nodeName, indent))
                if hasEnd(nodeName):
                    indent += 1
                nodeName = ""
                newNodeName = False
            elif newNodeName:
                nodeName += i
            elif i == "<":
                if len(innerText.strip(" "))>0 and not inNode:
                    self.nodes.append(inner(innerText,indent))
                innerText = ""
                
                inNode = True
                newNodeName = True
            else:
                innerText += i

class propertiesPanel:
    def __init__(self):
        self.properties = {}
        self.selectedProperty = 0
        self.editing = False

    def escape(self):
        panel = nodeSelector

    def up(self):
        self.selectedProperty -= 1
        if self.selectedProperty < 0:
            self.selectedProperty = 0
        
    
    def down(self):
        self.selectedProperty += 1
        if self.selectedProperty > len(self.properties)-1:
            self.selectedProperty = len(self.properties)-1

    def getSelectedKey(self):
        return list(self.properties)[self.selectedProperty]

class node:
    def __init__(self, name, indent):
        self.name = name.split(" ", -1)[0]
        self.indent = indent
        self.parseProperties(" ".join(name.split(" ", -1)[1:]))
    
    def parseProperties(self,raw):
        self.properties = dict(re.findall(r'(\w+)="([^"]*)"', raw))

class inner:
    def __init__(self, name, indent):
        self.name = '"'+name+'"'
        self.indent = indent
        self.properties = {"name":name}


nodeSelector = inspectorPanel()
propertyEditor = propertiesPanel()
panel = nodeSelector