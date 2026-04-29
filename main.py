from blessed import Terminal
import sys
import file
import inspector
import network
import tagSearch
term = Terminal()



def render(text):
    for i in text[0:len(text)]:
        print(i)

def checkExtendedIndent(indents,index):
    for i in indents[index+1::]:
        if i == indents[index]:
            return True
        elif i < indents[index]:
            return False
        elif i > indents[index]:
            return True
    return True

def limitLineLength(string,maxLength):
    if len(string) > maxLength:
        return string[:maxLength-3] + "..."
    return string


def hyperlink(url, text):
    #    return f"\033]8;;{url}\033\\{text}\033]8;;\033\\"
    return f"\x1b]8;;{url}\x1b\\\x1b[4m{text}\x1b[0m\x1b]8;;\x1b\\"

inspector.nodeSelector.parse(file.getRaw())
indents = inspector.nodeSelector.getIndentList()
def main():
    with term.fullscreen(), term.cbreak():
        sys.stdout.write("\033[?25l")
        while True:
            key = term.inkey(timeout=0.005)

            if key:
                try:
                    if key == "j" or key.code == term.KEY_UP:
                        inspector.panel.up()
                    if key == "k" or key.code == term.KEY_DOWN:
                        inspector.panel.down()
                    if key.code == term.KEY_ENTER:
                        inspector.panel.enter()
                    if key.code == term.KEY_ESCAPE:
                        inspector.panel.escape()

                    inspector.panel.keyPress(key,term)
                except Exception as e:
                    file.debug = "error happened" + str(e)
            lines = [" "]*(term.height-2)
            if inspector.panel == inspector.nodeSelector:
                lines[0] = "Nodes".center(term.width//2,"─")

            for i in range(len(inspector.nodeSelector.nodes)):
                text = inspector.nodeSelector.nodes[i].name 
                if inspector.nodeSelector.editing and i == inspector.nodeSelector.selectedNode:
                    text = text[:inspector.nodeSelector.cursorPos] + "|" + text[inspector.nodeSelector.cursorPos:]
                if isinstance(inspector.nodeSelector.nodes[i],inspector.inner):
                    text = '"'+text+'"'  
                if len(inspector.nodeSelector.nodes) >= i+2 and checkExtendedIndent(indents,i):
                    lines[i+1] = " "+(inspector.nodeSelector.nodes[i].indent)*"│ "+"├─"+text
                else:
                    lines[i+1] = " "+(inspector.nodeSelector.nodes[i].indent)*"│ "+"└─"+text

            lines[inspector.nodeSelector.selectedNode+1] = ">" + lines[inspector.nodeSelector.selectedNode+1][1:]

            #Divider
            for l in range(len(lines)):
                if len(lines[l]) < term.width//2:
                    lines[l] = lines[l].ljust(term.width//2, " ")
                lines[l] += "│"
            if type(inspector.panel) == tagSearch.searchPanel:
                lines[0] += "Tag Search".center(term.width//2,"─")
                lines[1] += inspector.panel.search[:inspector.panel.cursorPos] + "|" + inspector.panel.search[inspector.panel.cursorPos:]
                for i in range(2,len(lines)):
                    if len(inspector.panel.results) > i-2:
                        if i-2 == inspector.panel.selection:
                            lines[i] += limitLineLength("> "+inspector.panel.results[i-2]["tag"]+" - "+inspector.panel.results[i-2]["description"],term.width//2)
                        else:
                            lines[i] += limitLineLength("  "+inspector.panel.results[i-2]["tag"]+" - "+inspector.panel.results[i-2]["description"],term.width//2)
            else:
                inspector.propertyEditor.properties = inspector.nodeSelector.nodes[inspector.nodeSelector.selectedNode].properties
                inspector.propertyEditor.selectedNode = inspector.nodeSelector.nodes[inspector.nodeSelector.selectedNode]
                if inspector.panel is inspector.propertyEditor:
                    lines[0] += "Inspector".center(term.width//2,"─")
                else:
                    lines[0] += "Inspector".center(term.width//2," ")
                idx = 0
                for key in inspector.propertyEditor.properties:
                    if key == inspector.propertyEditor.getSelectedKey() and inspector.panel == inspector.propertyEditor:
                        lines[idx+1] += ">"
                    else:
                        lines[idx+1] += " "
                    if key == inspector.propertyEditor.getSelectedKey() and inspector.propertyEditor.editing:
                        text = inspector.propertyEditor.properties[key]
                        lines[idx+1] += key + " : " + text[:inspector.propertyEditor.cursorPos] + "|" + text[inspector.propertyEditor.cursorPos:]
                    else:
                        if type(inspector.propertyEditor.properties[key]) == str:
                            lines[idx+1] += key + " : " + limitLineLength( inspector.propertyEditor.properties[key], term.width//2-(len(key)+4))
                        elif type(inspector.propertyEditor.properties[key]) == bool:
                            if inspector.propertyEditor.properties[key]:
                                lines[idx+1] += key + " : " + "●"
                            else:
                                lines[idx+1] += key + " : " + "○"

                    idx += 1
                

            lines[-1] = "Arrow keys to navigate | Enter to Edit | Press Esc to go back"
            url = "127.0.0.1:5090"
            lines.append("Webpage hosted at : "+hyperlink(url,url)+" "+str(file.debug))
            print(term.home + term.clear,end="",flush=True)
            render(lines)

main()