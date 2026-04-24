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
nodeSelector = inspector.inspectorPanel()
propertyEditor = inspector.propertiesPanel()
panel = nodeSelector

def main():
    with term.fullscreen(), term.cbreak():
        sys.stdout.write("\033[?25l")
        while True:
            key = term.inkey(timeout=0.01)

            if key:
                if key == "j" or key.code == term.KEY_UP:
                    panel.up()
                if key == "k" or key.code == term.KEY_DOWN:
                    panel.down()
                if key.code == term.KEY_ENTER:
                    panel.enter()
                if key.code == term.KEY_ESCAPE:
                    panel.escape()
                try:
                    panel.key(key)
                except:
                    pass
            lines = [" "]*(term.height-2)
            lines[0] = "Nodes".center(term.width//2," ")

            nodeSelector.parse(file.getRaw())
            indents = nodeSelector.getIndentList()
            for i in range(len(nodeSelector.nodes)):
                if len(nodeSelector.nodes) >= i+2 and checkExtendedIndent(indents,i):
                    lines[i+1] = " "+(nodeSelector.nodes[i].indent)*"│ "+"├─"+nodeSelector.nodes[i].name + str(nodeSelector.nodes[i].indent)
                else:
                    lines[i+1] = " "+(nodeSelector.nodes[i].indent)*"│ "+"└─"+nodeSelector.nodes[i].name + str(nodeSelector.nodes[i].indent)

            lines[nodeSelector.selectedNode+1] = ">" + lines[nodeSelector.selectedNode+1][1:]
            for l in range(len(lines)):
                if len(lines[l]) < term.width//2:
                    lines[l] = lines[l].ljust(term.width//2, " ")
                lines[l] += "│"
            
            propertyEditor.properties = nodeSelector.nodes[nodeSelector.selectedNode].properties
            lines[0] += "Inspector".center(term.width//2," ")
            idx = 0
            for key in propertyEditor.properties:
                if key == propertyEditor.getSelectedKey() and panel == propertyEditor:
                    lines[idx+1] += ">" + key + "    " + propertyEditor.properties[key]
                else:
                    lines[idx+1] += " " + key + "    " + propertyEditor.properties[key]
                idx += 1
            


            lines.append("Webpage hosted at : 127.0.0.1:8080")
            print(term.home + term.clear,end="",flush=True)
            render(lines)
            

main()