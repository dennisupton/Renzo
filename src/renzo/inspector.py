import re
import renzo.file as file
import renzo.inspector as inspector
import renzo.tagSearch as tagSearch

class inspectorPanel:
    def __init__(self):
        self.tags = []
        self.selectedtag = 0
        self.editing = False
        self.cursorPos = 0
        self.offset = 0
        
    
    def getIndentList(self):
        res = []
        for i in self.tags:
            res.append(i.indent)
        return res

    def up(self):
        if not self.editing:
            self.selectedtag -= 1
            if self.selectedtag < 0:
                self.selectedtag = 0
            if self.selectedtag < self.offset:
                self.offset -= 1
        
    def down(self):
        if not self.editing and self.selectedtag < len(self.tags)-1:
            if not self.selectedtag <= self.maxHeight+self.offset:
                self.offset += 1
            self.selectedtag += 1

    def enter(self):
        if not self.editing:
            global panel, propertyEditor,inner
            if isinstance(self.tags[self.selectedtag],inner):
                self.cursorPos = 0
                self.editing = True
            else:
                panel = propertyEditor
                propertiesPanel.selectedProperty = 0
        else:
            file.convertToString(tagSelector.tags)
            self.editing = False

    def escape(self):
        if self.editing:
            file.convertToString(tagSelector.tags)
            self.editing = False
    def keyPress(self,keyName,term):
        if self.editing:
            if keyName.code == term.KEY_LEFT and self.cursorPos >0:
                self.cursorPos -= 1
            elif keyName.code == term.KEY_RIGHT and self.cursorPos < len(self.getSelectedtag().name):
                self.cursorPos += 1
            elif keyName.code == term.KEY_BACKSPACE and self.editing and self.cursorPos > 0:
                self.tags[self.selectedtag].name = self.getSelectedtag().name[:self.cursorPos-1] + self.getSelectedtag().name[self.cursorPos:]
                self.cursorPos -= 1
            elif len(keyName) == 1 and keyName.isprintable():
                self.tags[self.selectedtag].name = self.getSelectedtag().name[:self.cursorPos] + keyName + self.getSelectedtag().name[self.cursorPos:]
                self.cursorPos += 1
        elif keyName == "n":
            global panel
            panel = tagSearch.tagSearch
        elif keyName == "i":
            self.tags.insert(self.selectedtag+1,inner("",self.tags[self.selectedtag].indent))
            self.selectedtag += 1
            self.cursorPos = 0
            self.editing = True
        elif keyName == "x":
            self.tags.pop(self.selectedtag)
        elif keyName == '\x1b[1;5B':  # ctrl+down
            temp = self.tags[self.selectedtag-1]
            self.tags.pop(self.selectedtag-1)
            self.tags.insert(self.selectedtag,temp)

        elif keyName == '\x1b[1;5A':  # ctrl+up
            temp = self.tags[self.selectedtag+1]
            self.tags.pop(self.selectedtag+1)
            self.tags.insert(self.selectedtag,temp)
        elif keyName == '\x1b[1;5C':  # ctrl+right
            global tags
            if (type(self.tags[self.selectedtag-1]) == tag and self.tags[self.selectedtag].indent <= self.tags[self.selectedtag-1].indent) or self.tags[self.selectedtag].indent < self.tags[self.selectedtag-1].indent:
                self.tags[self.selectedtag].indent += 1
        elif keyName == '\x1b[1;5D':  # ctrl+left
            if self.tags[self.selectedtag].indent>0:
                self.tags[self.selectedtag].indent -= 1
        elif keyName == '\x1b[1;6B':  # ctrl+shift+down
            temp = [self.tags[self.selectedtag-1]]
            self.tags.pop(self.selectedtag-1)
            done = False
            index = 0
            for i in self.tags[self.selectedtag-1::]:
                if not done:
                    if i.indent > temp[0].indent:
                        self.tags.pop(self.selectedtag-1)
                        temp.append(i)
                        index +=1
                    else:
                        done = True
            for i in temp[::-1]:
                self.tags.insert(index+self.selectedtag+1,i)
            self.selectedtag = index+self.selectedtag+1
        elif keyName == '\x1b[1;6A':  # ctrl+shift+up
            idx = self.selectedtag
            while (not self.tags[idx].indent <= self.tags[self.selectedtag-1].indent) and idx >0:
                idx -= 1
            self.selectedtag = idx
            file.debug = self.tags[self.selectedtag].name
            temp = [self.tags[self.selectedtag-1]]
            self.tags.pop(self.selectedtag-1)
            done = False
            index = 0
            for i in self.tags[self.selectedtag-1::]:
                if not done:
                    if i.indent > temp[0].indent:
                        self.tags.pop(self.selectedtag-1)
                        temp.append(i)
                        index +=1
                    else:
                        done = True
            for i in temp:
                self.tags.insert(index+self.selectedtag+1,i)
            self.selectedtag = index+self.selectedtag+1
        elif keyName == '\x1b[1;6C':  # ctrl+shift+right
            pass
        elif keyName == '\x1b[1;6D':  # ctrl+shift+left
            pass
        file.convertToString(self.tags)

    def getSelectedtag(self):
        return self.tags[self.selectedtag]

    def parse(self,html):
        html.replace("\n","")
        self.tags = []
        indent = 0
        newtagName = False
        tagName = ""
        tagProperties = ""
        innerText = ""
        intag = False
        global inner
        for i in html:
            if newtagName and i == "/":
                newtagName = False
                indent -= 1
            elif i =="/":
                indent -= 1
            elif newtagName and i == ">":
                intag = False
                self.tags.append(tag(tagName, indent))
                if file.hasEnd(tagName):
                    indent += 1
                tagName = ""
                newtagName = False
            elif newtagName:
                tagName += i
            elif i == "<":
                if len(innerText.strip(" "))>0 and not intag:
                    self.tags.append(inner(innerText,indent))
                innerText = ""
                
                intag = True
                newtagName = True
            else:
                innerText += i

class propertiesPanel:
    def __init__(self):
        self.properties = {}
        self.selectedtag = None
        self.selectedProperty = 0
        self.editing = False
        self.cursorPos = 0
        self.newProp = False
        self.newPropName = ""
    def escape(self):
        if self.editing:
            file.convertToString(inspector.tagSelector.tags)
            self.editing = False
        else:
            global panel, tagSelector
            panel = tagSelector
            self.selectedProperty = 0

    def enter(self):
        if self.editing == False:
            if type(self.properties[self.getSelectedKey()]) == str:
                self.editing = True
                self.cursorPos = len(self.properties[self.getSelectedKey()])
            elif type(self.properties[self.getSelectedKey()]) == bool:
                self.properties[self.getSelectedKey()] = not self.properties[self.getSelectedKey()]
        else:
            if self.newProp:
                self.newProp = False
                self.selectedtag.properties[self.newPropName] = ""
            else:
                file.convertToString(inspector.tagSelector.tags)
            self.editing = False
    def keyPress(self,keyName,term):
        if keyName.code == term.KEY_LEFT and self.cursorPos >0:
            self.cursorPos -= 1
        elif keyName.code == term.KEY_RIGHT and self.editing and ((self.newProp and  self.cursorPos < len(self.newPropName)) or (not self.newProp and  self.cursorPos < len(self.properties[self.getSelectedKey()]))):
            self.cursorPos += 1
        elif keyName.code == term.KEY_BACKSPACE and self.editing and self.cursorPos >0:
            if self.newProp:
                self.newPropName = self.newPropName[:self.cursorPos-1] + self.newPropName[self.cursorPos:]
                self.cursorPos -=  1
            else:
                self.selectedtag.properties[self.getSelectedKey()] = self.properties[self.getSelectedKey()][:self.cursorPos-1] + self.properties[self.getSelectedKey()][self.cursorPos:]
                self.cursorPos -= 1
        if len(keyName) == 1 and keyName.isprintable() and self.editing:
            if self.newProp:
                self.newPropName = self.newPropName[:self.cursorPos] + keyName + self.newPropName[self.cursorPos:]
                self.cursorPos += 1
            else:
                self.selectedtag.properties[self.getSelectedKey()] = self.properties[self.getSelectedKey()][:self.cursorPos] + keyName + self.properties[self.getSelectedKey()][self.cursorPos:]
                self.cursorPos += 1
        elif keyName == "x":
            self.selectedtag.properties.pop(self.getSelectedKey())
            self.selectedProperty -= 1
        elif keyName == "n":
            self.newProp = True
            self.newPropName = ""
            self.editing = True
            self.cursorPos = 0
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

class tag:
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


tagSelector = inspectorPanel()
propertyEditor = propertiesPanel()
panel = tagSelector