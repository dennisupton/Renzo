from blessed import Terminal
import sys
import file
import inspector
import network

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

def main():
    with term.fullscreen(), term.cbreak():
        sys.stdout.write("\033[?25l")
        while True:
            key = term.inkey(timeout=0.01)

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

                    inspector.panel.key(key)
                except:
                    pass
            lines = [" "]*(term.height-2)
            lines[0] = "Nodes".center(term.width//2," ")

            inspector.nodeSelector.parse(file.getRaw())
            indents = inspector.nodeSelector.getIndentList()
            for i in range(len(inspector.nodeSelector.nodes)):
                if len(inspector.nodeSelector.nodes) >= i+2 and checkExtendedIndent(indents,i):
                    lines[i+1] = " "+(inspector.nodeSelector.nodes[i].indent)*"│ "+"├─"+inspector.nodeSelector.nodes[i].name + str(inspector.nodeSelector.nodes[i].indent)
                else:
                    lines[i+1] = " "+(inspector.nodeSelector.nodes[i].indent)*"│ "+"└─"+inspector.nodeSelector.nodes[i].name + str(inspector.nodeSelector.nodes[i].indent)

            lines[inspector.nodeSelector.selectedNode+1] = ">" + lines[inspector.nodeSelector.selectedNode+1][1:]
            for l in range(len(lines)):
                if len(lines[l]) < term.width//2:
                    lines[l] = lines[l].ljust(term.width//2, " ")
                lines[l] += "│"
            
            inspector.propertyEditor.properties = inspector.nodeSelector.nodes[inspector.nodeSelector.selectedNode].properties
            lines[0] += "Inspector".center(term.width//2," ")
            idx = 0
            for key in inspector.propertyEditor.properties:
                if key == inspector.propertyEditor.getSelectedKey() and inspector.panel == inspector.propertyEditor:
                    lines[idx+1] += ">" + key + "    " + inspector.propertyEditor.properties[key]
                else:
                    lines[idx+1] += " " + key + "    " + inspector.propertyEditor.properties[key]
                idx += 1
            


            lines.append("Webpage hosted at : 127.0.0.1:8080")
            print(term.home + term.clear,end="",flush=True)
            render(lines)
            

main()