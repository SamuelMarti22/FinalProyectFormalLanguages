import pandas as pd

from Rule import Rule
from State import State


def print_rules(rules):
    for rule in rules:
        print(f"{rule.get_simbolo_produccion()} -> {rule.get_produccion()}")

def print_strings(strings):
    for string in strings:
        print(string)

def identify_terminal(production):
    # Implementación de la función identify_terminal
    for i in range(len(production)):
        if production[i].isupper() and production[i] not in noTerminales:
            noTerminales.append(production[i])
        elif production[i] not in noTerminales and production[i] not in terminales:
            terminales.append(production[i])

def first(production,diccFirst,flagLL):
    # Implementación de la función first
    simbolo = production.get_produccion()[0]

    if simbolo == production.get_simbolo_produccion():
        print("Recursion por la izquieda")
        flagLL = False
        print("Flag LL: ", flagLL)
        production.set_first(".")
    else:
        if simbolo in terminales:
            production.set_first(simbolo)
            if simbolo not in diccFirst[production.get_simbolo_produccion()]:
                diccFirst[production.get_simbolo_produccion()].append(simbolo)
            else:
                flagLL = False
        else:
            production.set_first(diccFirst[simbolo])
            if simbolo not in diccFirst[production.get_simbolo_produccion()]:
                diccFirst[production.get_simbolo_produccion()].extend(diccFirst[simbolo])
                diccFirst[production.get_simbolo_produccion()] = list(set(diccFirst[production.get_simbolo_produccion()]))
    return flagLL

def follow(diccFollow,noTerminal):
    for i in range(len(reglas)):
        if noTerminal in reglas[i].get_produccion():
            posicion = reglas[i].get_produccion().index(noTerminal)
            if posicion == len(reglas[i].get_produccion())-1:
                if reglas[i].get_simbolo_produccion() == noTerminal:
                    diccFollow[noTerminal].extend(diccFollow[reglas[i].get_simbolo_produccion()])
                elif diccFollow[reglas[i].get_simbolo_produccion()] != [] and diccFollow[reglas[i].get_simbolo_produccion()] != ["$"]:
                    diccFollow[noTerminal].extend(diccFollow[reglas[i].get_simbolo_produccion()])
                elif reglas[i].get_simbolo_produccion() != noTerminal:
                    diccFollow[noTerminal].extend(follow(diccFollow, reglas[i].get_simbolo_produccion()))
                diccFollow[noTerminal] = list(set(diccFollow[noTerminal]))
            elif reglas[i].get_produccion()[posicion+1] in terminales:
                diccFollow[noTerminal].append(reglas[i].get_produccion()[posicion+1])
                diccFollow[noTerminal] = list(set(diccFollow[noTerminal]))
            else:
                firstNext = diccFirst[reglas[i].get_produccion()[posicion+1]].copy()
                if "e" in firstNext:
                    firstNext.remove("e")
                    if diccFollow[reglas[i].get_produccion()[posicion+1]] != []:
                        firstNext.extend(diccFollow[reglas[i].get_produccion()[posicion+1]])
                    else:
                        firstNext.extend(follow(diccFollow, reglas[i].get_produccion()[posicion+1]))
                diccFollow[noTerminal].extend(firstNext)
                diccFollow[noTerminal] = list(set(diccFollow[noTerminal]))
    return diccFollow[noTerminal]

def construccionTablaLL(diccFirst, diccFollow,regla):
    # Implementación de la función para construir la tabla LL(1)
    if "e" in regla.get_first():
        for i in range(len(diccFollow[regla.get_simbolo_produccion()])):
            parsingTableLL[(regla.get_simbolo_produccion(), diccFollow[regla.get_simbolo_produccion()][i])] = regla.get_produccion()
    else:
        for i in range(len(regla.get_first())):
            parsingTableLL[(regla.get_simbolo_produccion(), regla.get_first()[i])] = regla.get_produccion()

def searchRules(rules, symbol):
    listaReturn = []
    for i in rules:
        if i.get_simbolo_produccion() == symbol:
            x = Rule(symbol,"."+i.get_produccion())
            if x.get_produccion()[1] in noTerminales:
                listaReturn.append(x)
                if i.get_produccion()[0] != symbol:
                    listaReturn.extend(searchRules(rules, x.get_produccion()[1]))
            else:
                listaReturn.append(x)
    return listaReturn

def movePoint(regla):
    listaReglas = []
    produccion = regla.get_produccion()
    posicionPunto = regla.get_produccion().index(".")
    newProduction = produccion[:posicionPunto] + produccion[posicionPunto+1] + "." + produccion[posicionPunto+2:]
    try:
        posicionPunto = newProduction.index(".")
        newSymbol = newProduction[posicionPunto + 1]
        if newSymbol in noTerminales:
            listaReglas.extend(searchRules(reglas,newSymbol))
    except ValueError:
        newSymbol = None
    except IndexError:
        newSymbol = None
    newRule = Rule(regla.get_simbolo_produccion(),newProduction)
    listaReglas.append(newRule)
    return listaReglas

def identify_point(producciones, symbolTransition):
    reglasCumple = []
    for i in producciones:
        posicion = i.get_produccion().index(".")
        if posicion < len(i.get_produccion())-1:
            if i.get_produccion()[posicion+1] == symbolTransition:
                reglasCumple.append(i)
    for i in reglasCumple:
        producciones.remove(i)
    return reglasCumple

def createStateSRL(state):
    global numeroEstado
    pilaEstados = []
    pilaEstados.append(state)
    i = 0
    SLRStates = []
    while not pilaEstados == []:
        stateActual = pilaEstados.pop(0)
        producciones = stateActual.get_set_rules().copy()
        while i < len(producciones):
            posicionPunto = producciones[i].get_produccion().index(".")
            if posicionPunto == len(producciones[i].get_produccion())-1:
                producciones.remove(producciones[i])
            else:
                symbolTransition = producciones[i].get_produccion()[posicionPunto+1]
                listaSiguiente = identify_point(producciones,symbolTransition)
                puntosMovidos = []
                reglasMovidas = []
                for pm in range(len(listaSiguiente)):
                    puntosMovidos.extend(movePoint(listaSiguiente[pm]))
                for j in puntosMovidos:
                    reglasMovidas.append(j.get_produccion())
                if  any(set(reglasMovidas) == set(movimiento[1]) for movimiento in movimientosHechos):
                    for movimiento in movimientosHechos:
                        if set(reglasMovidas) == set(movimiento[1]):
                            numeroEstadoPrevio = movimiento[0]
                            break
                    if symbolTransition in noTerminales:
                        parsingTableSLR[(stateActual.get_number_state(), symbolTransition)] = numeroEstadoPrevio
                    else:
                        parsingTableSLR[(stateActual.get_number_state(), symbolTransition)] = f"d{numeroEstadoPrevio}"
                else:
                    newState = State(numeroEstado,puntosMovidos)
                    movimientosHechos.append([numeroEstado,reglasMovidas])
                    newState.set_previus_state(stateActual.get_number_state())
                    newState.set_symbol(symbolTransition)
                    SLRStates.append(newState)
                    pilaEstados.append(newState)
                    numeroEstado+=1
    return SLRStates

def printStates(listaEstadosResultantes,tamano):
    for i in listaEstadosResultantes[:tamano]:
        print(f"Estado {i.get_number_state()}: {i.get_previus_state()} -> {i.get_symbol()}")
        for j in i.get_set_rules():
            print(j.get_simbolo_produccion(),"->",j.get_produccion())



def construccionTablaSLR(diccFollow, listaEstadosResultantes):
    global flagSLR
    for i in listaEstadosResultantes:
        if i.get_symbol() in noTerminales:
            if (i.get_previus_state(), i.get_symbol()) not in parsingTableSLR:
                parsingTableSLR[(i.get_previus_state(), i.get_symbol())] = i.get_number_state()
            else:
                flagSLR = False
        else:
            if (i.get_previus_state(), i.get_symbol()) not in parsingTableSLR:
                parsingTableSLR[(i.get_previus_state(), i.get_symbol())] = f"d{i.get_number_state()}"
            else:
                flagSLR = False
        for j in i.get_set_rules():
            if j.get_produccion()[-1] == ".":
                reglaFinal = j.get_produccion().rstrip(".")
                for k in reglas:
                    if reglaFinal == k.get_produccion():
                        for l in diccFollow[k.get_simbolo_produccion()]:
                            if (i.get_number_state(), l) not in parsingTableSLR:
                                parsingTableSLR[(i.get_number_state(),l)] = f"r{reglas.index(k)}"
                            else:
                                flagSLR = False
                            
def createHistory()
    
def processSLR (string):
    if stack == 1 and string == "$":
        flagProcessSLR = True
        return flagProcessSLR
    charProcess = string[0]
    resultTable = parsingTableSLR[stack[-1],charProcess]

    
    


def print_parsing_table(parsingTableLL):
    # Filas y columnas
    filas = sorted({k[0] for k in parsingTableLL})
    columnas = sorted({k[1] for k in parsingTableLL})

    # Crear DataFrame
    #df = pd.DataFrame('', index=filas, columns=columnas)
    #for (fila, col), valor in parsingTableLL.items():
        #df.at[fila, col] = valor

    # Reemplazar celdas vacías con '-'
    #df.replace('', '-', inplace=True)

    # Imprimir con líneas
    #print(df.to_markdown(tablefmt="grid"))

reglas = []
strings = []
terminales = ['$']
noTerminales = []
flagLL= True
flagSLR= True
parsingTableLL = {}
parsingTableSLR = {}
SLRStates = []
numeroEstado = 1
listaEstadosResultantes = []
movimientosHechos = []

stack = []
symbolHistory = []
inputHistory = []
actionHistory = []
stack = [0]
processedSymbols = []
flagProcessSLR = False



with open("input.txt", "r") as archivo:
    # 1. Leer cuántas reglas hay
    num_reglas = int(archivo.readline().strip())

    # 2. Leer las reglas
    for i in range(num_reglas):
        regla = archivo.readline().strip()
        # Separar la regla en partes
        partes = regla.split("->")
        # Limpiar espacios y asegurarse de que haya exactamente 2 partes
        if len(partes) == 2:
            partes = [parte.strip() for parte in partes]
        else:
            print("Y entonces papi? Sea serio")
        # Separar las diferentes reglas en la parte derecha
        partes[1] = partes[1].split(" ")

        if i == 0:
            primero = partes[0]

        # Crear una regla para cada producción
        for j in range(len(partes[1])):
            identify_terminal(partes[0])
            identify_terminal(partes[1][j])
            rule = Rule(partes[0], partes[1][j])
            reglas.append(rule)

    # 3. Leer los strings hasta encontrar "e"
    for linea in archivo:
        linea = linea.strip()+"$"
        if linea == "e$":
            break
        strings.append(linea)

# Mostrar para verificar
print("Reglas:")
print_rules(reglas)
print("Strings:")
print_strings(strings)

diccFirst = {}
diccFollow = {}
for i in range(len(noTerminales)):
    diccFirst[noTerminales[i]] = []
    diccFollow[noTerminales[i]] = []
    if noTerminales[i] == primero:
        diccFollow[noTerminales[i]].append("$")

for i in range (len(reglas)-1,-1,-1):
    flagLL=first(reglas[i],diccFirst,flagLL)

print("Diccionario FIRST:")
print(diccFirst)

for simbolo in noTerminales:
    if diccFollow[simbolo] == [] or diccFollow[simbolo] == ["$"]:
        follow(diccFollow, simbolo)

#Revisar LL(1)
if not flagLL:
    print("No es LL(1)")
else:
    for i in noTerminales:
        if "e" in diccFirst[i] and flagLL:
            for j in range(len(reglas)):
                if reglas[j].get_simbolo_produccion() == i:
                    if reglas[j].get_first() in diccFollow[i]:
                        flagLL= False
                        print("Ambiguedad")
                        break

if flagLL:
    for i in range(len(reglas)):
        construccionTablaLL(diccFirst,diccFollow,reglas[i])

#Construccion de tabla para SLR(1)

#Creación manual del estado 0
reglaInicial = Rule(primero+"'","."+primero)
inicialProduccion = searchRules(reglas, primero)
inicialProduccion.insert(0,reglaInicial)
inicial = State(0,inicialProduccion)
parsingTableSLR[(1, "$")] = "accept"
listaEstadosResultantes.extend(createStateSRL(inicial))
tamano=len(listaEstadosResultantes)
print("ListaEstados:", len(listaEstadosResultantes))
printStates(listaEstadosResultantes,tamano)
print("Terminales:")
print(terminales)
print("No terminales:")
print(noTerminales)
print("Diccionario FIRST:")
print(diccFirst)
print("Diccionario FOLLOW:")
print(diccFollow)
print("Tabla LL(1):")
print_parsing_table(parsingTableLL)
print("Tabla SLR(1):")
construccionTablaSLR(diccFollow, listaEstadosResultantes)
print(parsingTableSLR)
print("Es LL(1)? ", flagLL)
print("Es SLR? ", flagSLR)