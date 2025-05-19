from graphviz import Digraph


def dibujar_arbol_LL(rules, symbolHistory):
    dot = Digraph(comment='Árbol de Derivación')
    rulesNodes={}
    idNodes=[]

    for i in rules:
        symbol = i.get_production_symbol()
        for j in range(len(idNodes) - 1, -1, -1):
            try:
                if symbol == idNodes[j][0]:
                    lastSymbolId = idNodes[j]
                    break
            except IndexError:
                symbolId = symbol + str(int(lastSymbolId[1:]) + 1)
                idNodes.append(symbolId)
                break
        

        
        print (rulesNodes)

def dibujar_arbol2():
    dot = Digraph()
    # Nodos
    dot.node('E0', 'E')
    dot.node('E1', 'E')
    dot.node('plus', '+')
    dot.node('T0', 'T')
    dot.node('T1', 'T')
    dot.node('F0', 'F')
    dot.node('i0', 'i')
    dot.node('F1', 'F')
    dot.node('parenL', '(')
    dot.node('E2', 'E')
    dot.node('parenR', ')')
    dot.node('T2', 'T')
    dot.node('T3', 'T')
    dot.node('star', '*')
    dot.node('F2', 'F')
    dot.node('F3', 'F')
    dot.node('i1', 'i')
    dot.node('i2', 'i')
    # Edges
    dot.edge('E0', 'E1')
    dot.edge('E0', 'plus')
    dot.edge('E0', 'T0')
    dot.edge('E1', 'T1')
    dot.edge('T1', 'F0')
    dot.edge('F0', 'i0')
    dot.edge('T0', 'F1')
    dot.edge('F1', 'parenL')
    dot.edge('F1', 'E2')
    dot.edge('F1', 'parenR')
    dot.edge('E2', 'T2')
    dot.edge('T2', 'star')
    dot.edge('T2', 'T3')
    dot.edge('T2', 'F3')
    dot.edge('T3', 'F2')
    dot.edge('F2', 'i1')
    dot.edge('F3', 'i2')
    dot.render('arbol', view=True, format="png")  # Esto crea y abre el archivo

