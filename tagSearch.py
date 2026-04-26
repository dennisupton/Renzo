import json
import file
import inspector

with open('htmlTags.json') as f:
    tags = json.load(f)

class searchPanel:
    def __init__(self):
        self.selection = 0
        self.search = ""
        self.results = tags
        self.cursorPos = 0

    def up(self):
        self.selection -= 1
        if self.selection < 0:
            self.selection = 0
        
    def down(self):
        self.selection += 1
        if self.selection > len(self.results)-1:
            self.selection = len(self.results)-1

    def enter(self):
        inspector.panel = inspector.nodeSelector
        indent = inspector.nodeSelector.nodes[inspector.nodeSelector.selectedNode].indent + 1
        inspector.nodeSelector.nodes.insert(inspector.nodeSelector.selectedNode+1,inspector.node(self.results[self.selection]["tag"],indent))
        file.convertToString()


    def escape(self):
        inspector.panel = inspector.nodeSelector
        
    def keyPress(self,keyName,term):
        if keyName.code == term.KEY_LEFT and self.cursorPos >0:
            self.cursorPos -= 1
        elif keyName.code == term.KEY_RIGHT and self.cursorPos < len(self.search):
            self.cursorPos += 1
        elif keyName.code == term.KEY_BACKSPACE and self.cursorPos > 0:
            self.search = self.search[:self.cursorPos-1] + self.search[self.cursorPos:]
            self.cursorPos -= 1
        elif len(keyName) == 1 and keyName.isprintable():
            self.search = self.search[:self.cursorPos] + keyName + self.search[self.cursorPos:]
            self.cursorPos += 1
        self.getSearchResults()
        self.selection = max(min(len(self.results)-1,self.selection),0)
    def getSearchResults(self):
        res = []
        for i in tags:
            if self.search in i["tag"]:
                res.append(i)
        self.results = res

nodeSearch = searchPanel()