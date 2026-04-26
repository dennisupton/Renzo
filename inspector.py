import re
import file
import inspector


class inspectorPanel:
    def __init__(self):
        self.nodes = []
        self.selectedNode = 0
        self.editing = False
        self.cursorPos = 0
    
    def getIndentList(self):
        res = []
        for i in self.nodes:
            res.append(i.indent)
        return res

    def up(self):
        if not self.editing:
            self.selectedNode -= 1
            if self.selectedNode < 0:
                self.selectedNode = 0
        
    def down(self):
        if not self.editing:
            self.selectedNode += 1
            if self.selectedNode > len(self.nodes)-1:
                self.selectedNode = len(self.nodes)-1

    def enter(self):
        if not self.editing:
            global panel, propertyEditor,inner
            if isinstance(self.nodes[self.selectedNode],inner):
                self.cursorPos = 0
                self.editing = True
            else:
                panel = propertyEditor
                propertiesPanel.selectedProperty = 0
        else:
            file.convertToString(nodeSelector.nodes)
            self.editing = False

    def escape(self):
        if self.editing:
            file.convertToString(nodeSelector.nodes)
            self.editing = False
    def keyPress(self,keyName,term):
        if self.editing:
            if keyName.code == term.KEY_LEFT and self.cursorPos >0:
                self.cursorPos -= 1
            elif keyName.code == term.KEY_RIGHT and self.cursorPos < len(self.getSelectedNode().name):
                self.cursorPos += 1
            elif keyName.code == term.KEY_BACKSPACE and self.editing:
                self.nodes[self.selectedNode].name = self.getSelectedNode().name[:self.cursorPos-1] + self.getSelectedNode().name[self.cursorPos:]
                self.cursorPos -= 1
            elif len(keyName) == 1 and keyName.isprintable():
                self.nodes[self.selectedNode].name = self.getSelectedNode().name[:self.cursorPos] + keyName + self.getSelectedNode().name[self.cursorPos:]
                self.cursorPos += 1
    
    def getSelectedNode(self):
        return self.nodes[self.selectedNode]

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
                if file.hasEnd(nodeName):
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
        self.selectedNode = None
        self.selectedProperty = 0
        self.editing = False

    def escape(self):
        global panel, nodeSelector
        panel = nodeSelector
        self.selectedProperty = 0
    
    def enter(self):
        if self.editing == False:
            self.editing = True
            self.cursorPos = len(self.properties[self.getSelectedKey()])
    
    def keyPress(self,keyName,term):

        if keyName.code == term.KEY_LEFT and self.cursorPos >0:
            self.cursorPos -= 1
        elif keyName.code == term.KEY_RIGHT and self.cursorPos < len(self.properties[self.getSelectedKey()]):
            self.cursorPos += 1
        elif keyName.code == term.KEY_BACKSPACE and self.editing:
            self.selectedNode.properties[self.getSelectedKey()] = self.properties[self.getSelectedKey()][:self.cursorPos-1] + self.properties[self.getSelectedKey()][self.cursorPos:]
            self.cursorPos -= 1
        elif keyName.code == term.KEY_ENTER and self.editing:
            return
        elif keyName.code == term.KEY_ESCAPE and self.editing:
            file.convertToString(inspector.nodeSelector.nodes)
            self.editing = False
        elif not keyName.code in [term.KEY_LEFT,term.KEY_RIGHT,term.KEY_BACKSPACE]:
            self.selectedNode.properties[self.getSelectedKey()] = self.properties[self.getSelectedKey()][:self.cursorPos] + keyName + self.properties[self.getSelectedKey()][self.cursorPos:]
            self.cursorPos += 1
            
    def up(self):
        self.selectedProperty -= 1
        if self.selectedProperty < 0:
            self.selectedProperty = 0
        
    
    def down(self):
        self.selectedProperty += 1
        if self.selectedProperty > len(self.properties)-1:
            self.selectedProperty = len(self.properties)-1

    def getSelectedKey(self):
        return str(list(self.properties)[self.selectedProperty])

class node:
    def __init__(self, name, indent):
        self.name = name.split(" ", -1)[0]
        self.indent = indent
        self.parseProperties(" ".join(name.split(" ", -1)[1:]))
    
    

    def parseProperties(self,raw):
        matches = re.findall(r'(\w+)(?:="([^"]*)")?', raw)
        self.properties = {k: (v if v != '' else True) for k, v in matches}

class inner:
    def __init__(self, name, indent):
        self.name = name
        self.indent = indent
        self.properties = {}


nodeSelector = inspectorPanel()
propertyEditor = propertiesPanel()
panel = nodeSelector