from blessed import Terminal
import sys
import file
import inspector
term = Terminal()



def render(text):
    for i in text[0:len(text)-10]:
        print(i)



inspector = inspector.inspectorPanel()


def main():
    with term.fullscreen(), term.cbreak():
        sys.stdout.write("\033[?25l")
        while True:
            key = term.inkey(timeout=0.01)

            if key:
                if key == "j" or key.code == term.KEY_UP:
                    inspector.up()
                if key == "k" or key.code == term.KEY_DOWN:
                    inspector.down()

            lines = [" "]*(term.height-1)
            lines[0] = "Nodes".center(term.width//2," ")

            inspector.parse(file.getRaw())

            for i in range(len(inspector.nodes)):
                if inspector.nodes[i].indent > 0:
                    if len(inspector.nodes) >= i+2 and inspector.nodes[i+1].indent == inspector.nodes[i].indent:
                        lines[i+1] = " ├─"+inspector.nodes[i].name
                    else:
                        lines[i+1] = " └─"+inspector.nodes[i].name
                else:
                    lines[i+1] = " "+inspector.nodes[i].name
            lines[inspector.selectedNode+1] = ">" + lines[inspector.selectedNode+1][1:]
            for l in range(len(lines)):
                if len(lines[l]) < term.width//2:
                    lines[l] = lines[l].ljust(term.width//2, " ")
                lines[l] += "│"

            lines[0] += "Inspector".center(term.width//2," ")
            idx = 0
            for key in inspector.nodes[inspector.selectedNode].properties:
                lines[idx+1] += key + inspector.nodes[inspector.selectedNode].properties[key]
                idx += 1
            print(term.home + term.clear,end="",flush=True)
            render(lines)

main()