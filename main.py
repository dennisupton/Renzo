from blessed import Terminal
import sys
import file
term = Terminal()


def render(text):
    for i in text[0:len(text)-10]:
        print(i)

def hasEnd(node):
    if node.startswith("!DOCTYPE") or node.startswith("html") or node.startswith("meta"):
        return False
    return True

def main():
    with term.fullscreen(), term.cbreak():
        sys.stdout.write("\033[?25l")
        while True:
            key = term.inkey(timeout=0.01)
            lines = [" "]*(term.height-1)
            lines[0] = "Nodes".center(term.width//2," ")
            nodes = []
            indents = []
            indent = 0
            newNodeName = False
            nodeName = ""
            for i in file.getRaw():
                if i == "<":
                    newNodeName = True
                elif newNodeName and i == "/":
                    newNodeName = False
                    indent -= 1
                elif i =="/":
                    indent -= 1
                elif newNodeName and i == ">":
                    nodes.append(nodeName)
                    indents.append(indent)
                    if hasEnd(nodeName):
                        indent += 1
                    nodeName = ""
                    newNodeName = False
                elif newNodeName:
                    nodeName += i
            for i in range(len(nodes)):
                if indents[i] > 0:
                    if len(indents) >= i+2 and indents[i+1] == indents[i]:
                        lines[i+1] = "├─"+nodes[i].split(' ', 1)[0]
                    else:
                        lines[i+1] = "└─"+nodes[i].split(' ', 1)[0]

                else:
                    lines[i+1] = nodes[i]

            for l in range(len(lines)):
                if len(lines[l]) < term.width//2:
                    lines[l] = lines[l].ljust(term.width//2, " ")
                lines[l] += "│"

            lines[0] += "Inspector".center(term.width//2," ")

            print(term.home + term.clear,end="",flush=True)
            render(lines)

main()