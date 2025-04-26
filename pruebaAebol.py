from graphviz import Digraph

def dibujar_arbol():
    dot = Digraph(comment='Árbol de Derivación')

    dot.node('S', 'S')
    dot.node('A', 'A')
    dot.node('B', 'B')
    dot.node('a', 'a')
    dot.node('b', 'b')

    dot.edges([('S', 'A'), ('S', 'B'), ('A', 'a'), ('B', 'b')])

    dot.render('arbol_derivacion', format='png', view=True)

dibujar_arbol()
