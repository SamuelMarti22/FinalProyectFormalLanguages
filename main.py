#Import libraries
import pandas as pd
from graphviz import Digraph

from pruebaArbol import dibujar_arbol_LL
from Rule import Rule
from State import State


#Print rules defined.
def print_rules(rules):
    for rule in rules:
        print(f"{rule.get_production_symbol()} -> {rule.get_production()}")

#Print rules defined.
def print_strings(strings):
    for string in strings:
        print(string)

#Identify terminals and non terminals of grammar in each production.
def identify_terminal(production):
    for i in range(len(production)):
        #Take each character, evaluate if it is capital and has not been add in nonTerminals.
        if production[i].isupper() and production[i] not in nonTerminals:
            nonTerminals.append(production[i])
        # If it not is capital then this character neither is non Terminal nor it is repet in terminals. Add this character in terminals.
        elif production[i] not in nonTerminals and production[i] not in terminals:
            terminals.append(production[i])

#Construction the first for every non terminal
def first(production,diccFirst,flagLL):
    #Take the first character in the production of a rule
    symbol = production.get_production()[0]
    #If the symbol is same the symbol of the production, then in the rule exist left recursion. Not is a grammar type LL(1)
    if symbol == production.get_production_symbol():
        print("Left Recursion")
        flagLL = False
        production.set_first(".")
    else:
        #Si el simbolo es un no terminal, lo agrega al first del simbolo de la produccion sino esta repetida
        if symbol in terminals:
            production.set_first(symbol)
            if symbol not in diccFirst[production.get_production_symbol()]:
                diccFirst[production.get_production_symbol()].append(symbol)
            else:
                flagLL = False
        else:
            #Si el simbolo es un no terminal es necesario agregar los simbolos del first de ese no terminal en the first del simbolo de la produccion
            production.set_first(diccFirst[symbol])
            if symbol not in diccFirst[production.get_production_symbol()]:
                diccFirst[production.get_production_symbol()].extend(diccFirst[symbol]) 
                #Elimina los simbolos repetidos tras ingresar los simbolos first correspondiente al otro simbolo
                diccFirst[production.get_production_symbol()] = list(set(diccFirst[production.get_production_symbol()])) 
    return flagLL

#Construccion de follow para cada no terminal 
def follow(diccFollow,nonTerminal):
    for i in range(len(rules)):
        #Encontrar en cada regla si es parte de ella
        if nonTerminal in rules[i].get_production():
            positionNonTerminal = rules[i].get_production().index(nonTerminal) #Toma la posicion donde se encuentra el non terminals
            #If the simbolo se encuentra en el final de la produccion
            if positionNonTerminal == len(rules[i].get_production())-1: 
                #Si la regla solo tiene al simbolo no terminal como produccion, agregar los simbolos del follow de este no terminal
                if rules[i].get_production_symbol() == nonTerminal:
                    diccFollow[nonTerminal].extend(diccFollow[rules[i].get_production_symbol()])
                #Si el follow de ese simbolo no terminal esta definido y es diferente de "$", agrega su valor al follow del simbolo de la regla donde se encuentra 
                elif diccFollow[rules[i].get_production_symbol()] != [] and diccFollow[rules[i].get_production_symbol()] != ["$"]:
                    diccFollow[nonTerminal].extend(diccFollow[rules[i].get_production_symbol()])
                #Si la produccion es diferente al simbolo no terminal, significa aun no tienen un follow definido; se hace recursion para definirlo y posteriormente agregarlo
                elif rules[i].get_production_symbol() != nonTerminal:
                    diccFollow[nonTerminal].extend(follow(diccFollow, rules[i].get_production_symbol()))
                diccFollow[nonTerminal] = list(set(diccFollow[nonTerminal])) #Elimina los caractetes repetidos tras agregarlos
            #Si el simbolo no terminal no se encuentra al final y esta seguido de un terminal, agrega este caracter a la lista de follows de simbolo no terminal
            elif rules[i].get_production()[positionNonTerminal+1] in terminals:
                diccFollow[nonTerminal].append(rules[i].get_production()[positionNonTerminal+1])
                diccFollow[nonTerminal] = list(set(diccFollow[nonTerminal]))  #Elimina los caractetes repetidos tras agregarlos
            else:
                #El simbolo no se encuentra al final y esta seguido de un no terminales, entonces debe agregarle los elementos del first de ese no terminal
                firstNext = diccFirst[rules[i].get_production()[positionNonTerminal+1]].copy()
                #Si los first incluyen el simbolo e, entoces debe de eliminarlo
                if "e" in firstNext:
                    firstNext.remove("e")
                    if diccFollow[rules[i].get_production()[positionNonTerminal+1]] != []:
                        #Existe un follow para este no terminal, entonces lo agrega
                        firstNext.extend(diccFollow[rules[i].get_production()[positionNonTerminal+1]]) 
                    else:
                        #No existe un follow para este no terminal, entonces debe realizar la recursion para encontrarlo y agregarlo
                        firstNext.extend(follow(diccFollow, rules[i].get_production()[positionNonTerminal+1])) 
                #Agrega los firts al follow del no terminal y elimina los caractetes repetidos
                diccFollow[nonTerminal].extend(firstNext)
                diccFollow[nonTerminal] = list(set(diccFollow[nonTerminal]))
    return diccFollow[nonTerminal] 

#Implementación de la función para construir la tabla LL(1)
def LLTableConstruction(diccFirst, diccFollow,rule):
    #Si el first de la regla tiene el caracter first, crea el diccionario con la tupla con los follows del simbolo de produccion de la regla
    if "e" in rule.get_first():
        for i in range(len(diccFollow[rule.get_production_symbol()])):
            parsingTableLL[(rule.get_production_symbol(), diccFollow[rule.get_production_symbol()][i])] = rule.get_production()
    else:
        #Crea el diccionario con la tupla del simbolo de produccion de la regla, su firts y la produccion
        for i in range(len(rule.get_first())):
            parsingTableLL[(rule.get_production_symbol(), rule.get_first()[i])] = rule.get_production()

#Busca las reglas que tienen un simbolo de produccion dado 
def searchRules(rules, symbol):
    listReturn = []
    # Itera sobre todas las reglas para encontrar coincidencias con el símbolo de producción.
    for i in rules:
        if i.get_production_symbol() == symbol:
            # Crea una nueva regla con el punto al principio de la producción.
            x = Rule(symbol,"."+i.get_production())
            #Si el segundo símbolo de la producción es un no terminal, agrega la regla y busca más reglas recursivamente.
            if x.get_production()[1] in nonTerminals:
                listReturn.append(x)
                if i.get_production()[0] != symbol:
                    listReturn.extend(searchRules(rules, x.get_production()[1]))
            else:
                #Al ser un terminal solo agrega la regla, ya que no genera una transicion a otra.
                listReturn.append(x)
    return listReturn

def movedot(rule):
    listrules = []
    # Obtiene la producción de la regla y localiza el punto en la producción.
    production = rule.get_production()
    dotPosition = rule.get_production().index(".")
    # Crea una nueva producción moviendo el punto un lugar adelante.
    newProduction = production[:dotPosition] + production[dotPosition+1] + "." + production[dotPosition+2:]
    # Intenta encontrar el nuevo símbolo después del punto y buscar más reglas recursivas si es un no terminal.
    try:
        dotPosition = newProduction.index(".")
        newSymbol = newProduction[dotPosition + 1]
        if newSymbol in nonTerminals:
            listrules.extend(searchRules(rules,newSymbol))
    except ValueError:
        # Si no encuentra un punto, se asigna None al nuevo símbolo.
        newSymbol = None
    except IndexError:
        # Si el índice está fuera de rango, se asigna None al nuevo símbolo.
        newSymbol = None
    # Crea una nueva regla con la producción modificada y la añade a la lista de reglas que componen cada estado. 
    newRule = Rule(rule.get_production_symbol(),newProduction)
    listrules.append(newRule)
    return listrules

def identify_dot(productions, symbolTransition):
    rulesRight = []
    # Itera sobre todas las producciones para encontrar las que tengan un punto antes de 'symbolTransition'.
    for i in productions:
        positionNonTerminal = i.get_production().index(".")
        # Verifica si el punto no está al final y si el siguiente símbolo es el de la transición.
        if positionNonTerminal < len(i.get_production())-1:
            if i.get_production()[positionNonTerminal+1] == symbolTransition:
                rulesRight.append(i)
    # Elimina las reglas que se han agregado a 'rulesRight' de la lista de producciones.
    for i in rulesRight:
        productions.remove(i)
    # Devuelve la lista de reglas que coinciden con la transición del símbolo.
    return rulesRight

def createStateSRL(state):
    #Define la variable global 'numberState' para llevar un conteo de los estados.
    global numberState
    stackStates = []
    stackStates.append(state)
    i = 0
    SLRStates = []
    #Recorre la lista de estados hasta que no haya más estados por procesar.
    while not stackStates == []:
        #Toma el primer estado de la lista de estados.
        stateActual = stackStates.pop(0)
        productions = stateActual.get_set_rules().copy()
        #Recorremos la lista de producciones para procesar cada producción.
        while i < len(productions):
            #Obtenemos la posición del punto en la producción.
            dotPosition = productions[i].get_production().index(".")
            #Si el punto está al final de la producción, se considera una reducción y se eliminan las producciones.
            if dotPosition == len(productions[i].get_production())-1:
                productions.remove(productions[i])
            else:
                #Si el punto no está al final, se obtiene el símbolo siguiente al punto.
                symbolTransition = productions[i].get_production()[dotPosition+1]
                #Se buscan todas las producciones que se pueden mover con ese símbolo.
                listnext = identify_dot(productions,symbolTransition)
                movedDots = []
                rulesMoved = []
                #Movemos el punto en las producciones que se pueden mover.
                for pm in range(len(listnext)):
                    movedDots.extend(movedot(listnext[pm]))
                #Llevamos un monitoreo de los movimientos realizados (útil para evitar duplicados y asignar desp)azamientos.
                for j in movedDots:
                    rulesMoved.append([j.get_production_symbol(),j.get_production()])
                #Si el símbolo de transición es un e, creamos directamente una reducción en la tabla.
                if symbolTransition == "e":
                    for k in rules:
                        if symbolTransition == k.get_production():
                            for l in diccFollow[k.get_production_symbol()]:
                                if (stateActual.get_number_state(), l) not in parsingTableSLR:
                                    parsingTableSLR[(stateActual.get_number_state(),l)] = f"r{rules.index(k)}"
                #Buscamos si las reglas que se han movido ya están en la lista de movimientos completados.
                #Si ya están, se asigna el número de estado correspondiente para el desplazamiento.
                if  any(set(tuple(r) for r in rulesMoved) == set(tuple(r) for r in movement[1]) for movement in movementsCompleted):
                    for movement in movementsCompleted:
                        if set(tuple(r) for r in rulesMoved) == set(tuple(r) for r in movement[1]):
                            numberStatePrevious = movement[0]
                            break
                    #Si el símbolo de transición es un no terminal, se asigna el número de estado directamente.
                    #Si no, se asigna un desplazamiento en la tabla de análisis.
                    if symbolTransition in nonTerminals:
                        parsingTableSLR[(stateActual.get_number_state(), symbolTransition)] = numberStatePrevious
                    else:
                        parsingTableSLR[(stateActual.get_number_state(), symbolTransition)] = f"d{numberStatePrevious}"
                else:
                    #Si no se ha encontrado el movimiento, se crea un nuevo estado con el número de estado correspondiente.
                    #Se asigna el símbolo de transición y se agrega a la lista de movimientos completados.
                    newState = State(numberState,movedDots)
                    movementsCompleted.append([numberState,rulesMoved])
                    newState.set_previus_state(stateActual.get_number_state())
                    newState.set_symbol(symbolTransition)
                    SLRStates.append(newState)
                    stackStates.append(newState)
                    numberState+=1
    return SLRStates

#Print states created from createStateSLR
def printStates(listStatesResultant,size):
    for i in listStatesResultant[:size]:
        print(f"State {i.get_number_state()}: {i.get_previus_state()} -> {i.get_symbol()}")
        for j in i.get_set_rules():
            print(j.get_production_symbol(),"->",j.get_production())

def SLRTableConstruction(diccFollow, listStatesResultant):
    global flagSLR
    # Itera sobre cada estado en la lista de estados resultantes.
    for i in listStatesResultant:
        # Si el símbolo es un no terminal, se agrega una transición o acción en la tabla de parsing.
        if i.get_symbol() in nonTerminals:
            # Si el símbolo es un no terminal, se agrega se asigna el número de estado directamente.
            if (i.get_previus_state(), i.get_symbol()) not in parsingTableSLR:
                parsingTableSLR[(i.get_previus_state(), i.get_symbol())] = i.get_number_state()
            # Si la transición ya existe (es decir, ya hay un desplazamiento o acción para ese estado y símbolo), se marca como ambigüedad.
            else:
                flagSLR = False
        else:
            # Si el símbolo es un terminal, se agrega un desplazamiento en la tabla de parsing.
            if (i.get_previus_state(), i.get_symbol()) not in parsingTableSLR:
                parsingTableSLR[(i.get_previus_state(), i.get_symbol())] = f"d{i.get_number_state()}"
            else:
            # Si la transición ya existe (es decir, ya hay un desplazamiento o acción para ese estado y símbolo), se marca como ambigüedad.
                flagSLR = False

        #Empezamos a revisar las reglas que tienen el punto al final de la producción.
        for j in i.get_set_rules():
            if j.get_production()[-1] == ".":
                ruleFinal = j.get_production().rstrip(".")
                for k in rules:
                    if ruleFinal == k.get_production():
                        # Si la producción es igual a la regla, se crea una acción de reducción con el index de lt.
                        for l in diccFollow[k.get_production_symbol()]:
                            if (i.get_number_state(), l) not in parsingTableSLR:
                                parsingTableSLR[(i.get_number_state(),l)] = f"r{rules.index(k)}"
                            # Si la acción ya existe (es decir, ya hay un desplazamiento o acción para ese estado y símbolo), se marca como ambigüedad.
                            else:
                                print(f"Ambiguity in the State {i.get_number_state()} with the rule {k.get_production_symbol()} -> {k.get_production()}")
                                flagSLR = False

#Agrega a las variables el historial respectivo que obtuvo en processedSLR.
def createHistoriesSLR(actionSymbol,stackSLRSymbol,inputSymbol,simbolsSymbol):
    actionHistory.append(actionSymbol)
    symbolHistory.append(list(simbolsSymbol))
    inputHistory.append(inputSymbol)
    stackSLRHistory.append(list(stackSLRSymbol)) #Invierto el stack para que se vea mejor en la tabla

#Proceso de validación de una cadena usando SLR
def processSLR (string,stackSLR,processedSymbols,flagProcessSLR):
    # Caso de aceptación: Si la pila contiene el valor 1 y el string es el símbolo de fin '$', termina el proceso con éxito.
    if stackSLR[-1] == 1 and string == "$":
        flagProcessSLR = True
        return flagProcessSLR
    # Intenta obtener la acción del diccionario parsing SLR usando la pila y el primer símbolo de la cadena.
    try:
        action = parsingTableSLR[stackSLR[-1],string[0]]
    except KeyError:
        #De no encontrarlo retorna la flag que  controla la validación, significando que la cadena no hacce parte del lenguaje
        return flagProcessSLR
    
    #Revisa si la acción es de desplazamiento
    if action[0] == "d":
            #Al ser desplazamiento, el caracter que se encuentra procesando se agregara a processedSymbols, debido a ser leido
            processedSymbols.append(string[0])
            newString = string[1:] #Elimina el caracter desplazado a processedSymbols de la cadena a procesar
            stackSLR.append(int(action[1:])) #Agrega al stack del proceso la accion
            createHistoriesSLR(action,stackSLR,newString,processedSymbols)
            return processSLR(newString,stackSLR,processedSymbols,flagProcessSLR) #Hace recursion para seguir procesando la cadena
    
    #Revisa si la acción es de reducción
    if action[0] == "r":
        derivacion=[]
        ruleReducce = rules[int(action[1:])]
        derivacion.append(ruleReducce.get_production_symbol())
        derivacion.append(ruleReducce.get_production())
        derivacionHistory.append(derivacion)
         #Busca la regla de reducciónn que usa la accion
        #Si la produccion de la regla es un epsilon, agregamos el simbolo de produccion a processedSymbols y al stack el estado resultante de esta accion.
        if ruleReducce.get_production() == "e":
            processedSymbols.append(ruleReducce.get_production_symbol())
            try:
                stackSLR.append(parsingTableSLR[stackSLR[-1],processedSymbols[-1]])
                createHistoriesSLR(action,stackSLR,string,processedSymbols)
                return processSLR(string,stackSLR,processedSymbols,flagProcessSLR)
            except KeyError:
                return flagProcessSLR
        else:
            #Al no ser un epsilon, debemos de reduccir los caracteres y los estados del stack respectivos a la regla 
            lengthRule = len(ruleReducce.get_production()) #Obtenemos el tamaño de la produccion de la regla respectiva para saber la cantidad de caracteres a reducir
            if len(processedSymbols) == lengthRule:
                processedSymbols.clear()
            else:
                processedSymbols = processedSymbols[:(len(processedSymbols)-lengthRule)] #Eliminamos de processedSymbols la cantidad de caracteres respectivos
            processedSymbols.append(ruleReducce.get_production_symbol())
            newString = string #En las reducciones no se modifica la cadena a procesar
            stackSLR = stackSLR[:(len(stackSLR)-lengthRule)] #Eliminamos del stack la cantidad de estados respectivos
            try:
                #Intenta obtener el estado resultante de hacer el Reduce
                stackSLR.append(parsingTableSLR[stackSLR[-1],processedSymbols[-1]])
            except KeyError:
                return flagProcessSLR
            createHistoriesSLR(action,stackSLR,newString,processedSymbols)
        return processSLR(newString,stackSLR,processedSymbols,flagProcessSLR)  #Hace recursion para seguir procesando la cadena

#Agrega a las variables el historial respectivo que obtuvo en processedLL.
def createHistoriesLL(stackSLRSymbol,inputSymbol):
    inputHistory.append(inputSymbol)
    stackSLRHistory.append(list(stackSLRSymbol)[::-1])

#Proceso de validación de una cadena usando SLR
def processLL(string,flagProcessLL):
    # Caso de aceptación: Si la pila contiene el valor "4" y el string es el símbolo de fin '$', termina el proceso con éxito.
    if stackLL[-1] == "$" and string == "$":
        #Vacia la pila y agrega el proceso al historial
        stackLL.pop(0)
        createHistoriesLL(stackLL,string)
        flagProcessLL = True
        return flagProcessLL
    #Si el ultimo simbolo de la pila coincide con el primero de la cadena, hace match, elimina los simbolos procesados 
    if stackLL[-1] == string[0]:
        string = string[1:]
        stackLL.pop(-1)
        createHistoriesLL(stackLL,string)
        return processLL(string,flagProcessLL)  #Hace recursion para seguir procesando la cadena
    else:
        #Trata de obtener los nuevos simbolos para el stack, que son el resultado de emparejar el ultimo simbolo del stack y el caracter de la cadena a procesar
        try:
            addStack = parsingTableLL[stackLL[-1],string[0]]
            derivación=[]
            derivación.append(stackLL[-1])
            derivación.append(addStack)
            derivacionHistory.append(derivación)
        except KeyError:
            return flagProcessLL
        stackLL.pop(-1) #Elimina el simbolo tomado por el emparejamiento
        addStack=addStack[::-1] #Invierte el resultado a ingresar en el stack
        stackLL.extend(addStack) #Agrega al stack esta variable
        #Si agrego un epsilo a la fila debe de eliminarlo, ya que representa el vacio
        if addStack[-1] == "e":
            stackLL.pop(-1)
            createHistoriesLL(stackLL,string)
            return processLL(string,flagProcessLL)
        else:
            createHistoriesLL(stackLL,string)
            return processLL(string,flagProcessLL) #Hace recursion para seguir procesando la cadena

#Función para imprimir las tablas de análisis sintáctico
def print_parsing_table(parsingTableLL):
    #rows y columns
    rows = sorted({k[0] for k in parsingTableLL})
    columns = sorted({k[1] for k in parsingTableLL})
    #Crear DataFrame
    df = pd.DataFrame('', index=rows, columns=columns)
    for (fila, col), valor in parsingTableLL.items():
        df.at[fila, col] = valor
    #Reemplazar celdas vacías con '-'
    df.replace('', '-', inplace=True)
    #Imprimir con líneas
    print(df.to_markdown(tablefmt="grid"))

#Función para imprimir el proceso de análisis sintáctico
def print_parsing_process_LL(stackSLRHistory, inputHistory, resutlLL):
    #Crear DataFrame
    df = pd.DataFrame({    "Stack": [" ".join(stack) for stack in stackSLRHistory],
    "Input": [" ".join(cadena) for cadena in inputHistory]})
    #Reemplazar celdas vacías con '-'
    df.replace('', '-', inplace=True)

    if resutlLL:
        resultado = "Cadena aceptada"
    else:
        resultado = "Cadena rechazada"
    df.loc[len(df.index)] = [resultado, "-----"]

    print(df.to_markdown(tablefmt="grid"))

def print_parsing_process_SLR(stackSLRHistory,symbolHistory, inputHistory, actionHistory,resutlSLR):
    #Crear DataFrame
    df = pd.DataFrame({"Stack": [" ".join(str(stack)) for stack in stackSLRHistory],
    "Symbols": [" ".join(stack) for stack in symbolHistory],
    "Input": [" ".join(cadena) for cadena in inputHistory],
    "Action": [" ".join(cadena) for cadena in actionHistory]})
    #Reemplazar celdas vacías con '-'
    df.replace('', '-', inplace=True)
    if resutlSLR:
        resultado = "Cadena aceptada"
    else:
        resultado = "Cadena rechazada"
    df.loc[len(df.index)] = [resultado, "-----","-----","-----"]
    print(df.to_markdown(tablefmt="grid"))

def dibujar_arbol_LL(rules):
    #dot = Digraph(comment='Árbol de Derivación')
    for i in range(len(rules)):
        if rules[i].get_production_symbol() == startSymbolGrammar and i == 0:
            for j in range(len(rules[i].get_production())):
                idNodes.append(rules[i].get_production()[j]+"0")
        else:
            j=0
            symbol = rules[i].get_production_symbol()
            for j in range(len(idNodes)):
                try:
                    if symbol == idNodes[j][0]:
                        lastSymbolId = idNodes[j]
                        if lastSymbolId not in idNodes:
                            idNodes.append(lastSymbolId)
                        break
                except IndexError:
                    break

            for j in range(len(rules[i].get_production())):
                flagTree=False
                symbolProductionId = rules[i].get_production()[j]
                for k in range(len(idNodes) - 1, -1, -1):
                    if symbolProductionId == idNodes[k][0]:
                        lastSymbolProduction = idNodes[k]
                        symbolProductionId = symbolProductionId + str(int(lastSymbolId[1:]) + 1)
                        idNodes.append(symbolProductionId)
                        flagTree=True
                        break
                if not flagTree:
                    idNodes.append(rules[i].get_production()[j]+"0")
    return idNodes


def print_tree_LL(derivationHistory, startSymbolGrammar):
    dot = Digraph(comment='Árbol de Derivación')
    derivacion = derivationHistory.copy()
    repeticion = {startSymbolGrammar: 0}
    actual = 0
    for i in derivacion:
        actual = repeticion[i[0]]
        for j in i[1]:
            if j in repeticion:
                repeticion[j] += 1
            else:
                repeticion[j] = 0
            dot.node(j+str(repeticion[j]), j)
            if j != i[0]:
                dot.edge(i[0]+str(actual), j+str(repeticion[j]))
            else:
                dot.edge(i[0]+str(actual), j+str(repeticion[j]))

    dot.render('arbol', view=True, format="png")  # Esto crea y abre el archivo
    #print(repeticion)
    #print(derivacion)
    print("--------------------------------------------------")
    #Nodos

#Definition of variables obtained from the input
rules = []
strings = []
terminals = ['$']
nonTerminals = []

#Definition of variables to make the SLR(1)
flagSLR= True
parsingTableSLR = {}
SLRStates = []
numberState = 1
listStatesResultant = []
movementsCompleted = []
symbolHistory = []
inputHistory = []
actionHistory = []
stackSLRHistory = []
stackSLR = [0]
processedSymbols = []
derivacionHistory = []
flagProcessSLR = False

#Definition of variables to make the LL(1)
stackLL = ["$"]
flagLL= True
parsingTableLL = {}
flagProcessLL = False

#Read the input file
with open("input.txt", "r") as file:
    #Read the first line of the file, which contains the number of rules
    num_rules = int(file.readline().strip())
    #Read each rule and store it in the rules list
    for i in range(num_rules):
        rule = file.readline().strip()
        parts = rule.split("->")
        #Confirma que la regla tiene el formato correcto (Simbolo de produccion -> Produccion)
        if len(parts) == 2:
            parts = [parte.strip() for parte in parts]
        else:
            print("Does not meet the requirements of the txt file")
            exit()
        #Separa las diferentes producciones de un mismo simbolo de produccion y los almacena en la lista de reglaso
        parts[1] = parts[1].split(" ")
        if i == 0:
            #Definimos el simbolo de inicio de la gramatica
            startSymbolGrammar = parts[0]
        #Identificamos los simbolos terminales y no terminales y los vamos agregando a sus respectivas listas
        for j in range(len(parts[1])):
            identify_terminal(parts[0])
            identify_terminal(parts[1][j])
            rule = Rule(parts[0], parts[1][j])
            rules.append(rule)
    #Leemos las cadenas a procesar y las almacenamos en la lista de cadenas, hasta encontrar el caracter "e"
    for line in file:
        line = line.strip()+"$"
        if line == "e$":
            break
        strings.append(line)

#Inicializamos la pila de análisis sintáctico y los diccionarios de FIRST y FOLLOW
stackLL.append(startSymbolGrammar)
diccFirst = {}
diccFollow = {}
for i in range(len(nonTerminals)):
    diccFirst[nonTerminals[i]] = []
    diccFollow[nonTerminals[i]] = []
    if nonTerminals[i] == startSymbolGrammar:
        diccFollow[nonTerminals[i]].append("$")

#Construimos el diccionario de FIRST para cada no terminal
for i in range (len(rules)-1,-1,-1):
    flagLL=first(rules[i],diccFirst,flagLL)

#Construimos el diccionario de FOLLOW para cada no terminal
for symbol in nonTerminals:
    if diccFollow[symbol] == [] or diccFollow[symbol] == ["$"]:
        follow(diccFollow, symbol)

# Check if the grammar is LL(1)
if not flagLL:
    print("It is not LL(1)")
else:
    # For each non-terminal symbol
    for i in nonTerminals:
        # If epsilon (empty string) is in its FIRST set and flagLL is still True
        if "e" in diccFirst[i] and flagLL:
            # Go through all the rules
            for j in range(len(rules)):
                # If the rule corresponds to the current non-terminal
                if rules[j].get_production_symbol() == i:
                    # Check for intersection between FIRST and FOLLOW sets
                    if rules[j].get_first() in diccFollow[i]:
                        flagLL = False
                        print("Ambiguity detected")
                        break

if flagLL:
    for i in range(len(rules)):
        LLTableConstruction(diccFirst,diccFollow,rules[i])

ruleinitial = Rule(startSymbolGrammar+"'","."+startSymbolGrammar)
initialproduction = searchRules(rules, startSymbolGrammar)
initialproduction.insert(0,ruleinitial)
initial = State(0,initialproduction)
parsingTableSLR[(1, "$")] = "accept"
listStatesResultant.extend(createStateSRL(initial))
if "e" in terminals:
    terminals.remove("e")
if "$" in terminals:
    terminals.remove("$")

print("Rules:")
print_rules(rules)
print("----------------------------------------------------------------")
print("Terminals:")
print(terminals)
print("----------------------------------------------------------------")
print("Non Terminals:")
print(nonTerminals)
print("----------------------------------------------------------------")
print("Diccionario FIRST:")
print(diccFirst)
print("----------------------------------------------------------------")
print("Diccionario FOLLOW:")
print(diccFollow)
print("----------------------------------------------------------------")
SLRTableConstruction(diccFollow, listStatesResultant)
print("Strings to be processed:")
for i in strings:
    print(i.rstrip("$"), end=" | ")
print("----------------------------------------------------------------")

if (flagLL and flagSLR):
    print("Select a parser (T: for LL(1), B: for SLR(1), Q: quit):")
    response = input()
    match response:
        case "T":
            print("Tabla LL(1):")
            print_parsing_table(parsingTableLL)
            for i in strings:
                resultLL = processLL(i,flagProcessLL)
                if resultLL:
                    print("The string: ",i," belongs to the grammar")
                    print("Press space to continue")
                    print_tree_LL(derivacionHistory,startSymbolGrammar)
                    s = input()
                else:
                    print("The string: ",i," not belongs to the grammar")
                print_parsing_process_LL(stackSLRHistory, inputHistory, resultLL)
                stackLL = ["$",startSymbolGrammar]
                inputHistory = []
                stackSLRHistory = []
                derivacionHistory = []
        case "B":
            print("Tabla SLR(1):")
            print_parsing_table(parsingTableSLR)
            for i in strings:
                result = processSLR(i,stackSLR,processedSymbols,flagProcessSLR)
                if result:
                    print("The string: ",i," belongs to the grammar")
                    derivacionHistory= derivacionHistory[::-1]
                    print_tree_LL(derivacionHistory,startSymbolGrammar)
                    print("Press space to continue")
                    s = input()
                else:
                    print("The string: ",i," not belongs to the grammar")
                print_parsing_process_SLR(stackSLRHistory,symbolHistory, inputHistory, actionHistory, result)
                stackSLR = [0]
                processedSymbols = []
                symbolHistory = []
                inputHistory = []
                stackSLRHistory = []
                actionHistory = []
                derivacionHistory = []
        case "Q":
            print("Bye ;)")
            exit()
        case _:
            print("Invalid option")
elif flagLL:
    print("Grammar is LL(1).")
    print("Tabla LL(1):")
    print_parsing_table(parsingTableLL)
    for i in strings:
        resultLL = processLL(i,flagProcessLL)
        if resultLL:
            print("The string: ",i," belongs to the grammar")
            print_tree_LL(derivacionHistory,startSymbolGrammar)
            print("Press space to continue")
            s = input()
        else:
            print("The string: ",i," not belongs to the grammar")
        print_parsing_process_LL(stackSLRHistory, inputHistory, resultLL)
        stackLL = ["$",startSymbolGrammar]
        inputHistory = []
        stackSLRHistory = []
        derivacionHistory = []

    print("Imprimir arbol")
    print_tree_LL(derivacionHistory,startSymbolGrammar)
elif flagSLR:
    
    print("Grammar is SLR(1).")
    print("Tabla SLR(1):")
    print_parsing_table(parsingTableSLR)
    for i in strings:
        result = processSLR(i,stackSLR,processedSymbols,flagProcessSLR)
        if result:
            print("The string: ",i," belongs to the grammar")
            derivacionHistory= derivacionHistory[::-1]
            print_tree_LL(derivacionHistory,startSymbolGrammar)
            print("Press space to continue")
            s = input()
        else:
            print("The string: ",i," not belongs to the grammar")
        print_parsing_process_SLR(stackSLRHistory,symbolHistory, inputHistory, actionHistory, result)
        stackSLR = [0]
        symbolHistory = []
        inputHistory = []
        processedSymbols = []
        stackSLRHistory = []
        actionHistory = []
        derivacionHistory = []
else:
    print("Grammar is neither LL(1) nor SLR(1).")