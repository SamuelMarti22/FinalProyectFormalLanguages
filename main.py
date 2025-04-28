import pandas as pd
from Rule import Rule
from State import State

def print_rules(rules):
    for rule in rules:
        print(f"{rule.get_production_symbol()} -> {rule.get_production()}")

def print_strings(strings):
    for string in strings:
        print(string)

def identify_terminal(production):
    for i in range(len(production)):
        if production[i].isupper() and production[i] not in nonTerminals:
            nonTerminals.append(production[i])
        elif production[i] not in nonTerminals and production[i] not in terminals:
            terminals.append(production[i])

def first(production,diccFirst,flagLL):
    symbol = production.get_production()[0]
    if symbol == production.get_production_symbol():
        print("Left Recursion")
        flagLL = False
        print("Flag LL: ", flagLL)
        production.set_first(".")
    else:
        if symbol in terminals:
            production.set_first(symbol)
            if symbol not in diccFirst[production.get_production_symbol()]:
                diccFirst[production.get_production_symbol()].append(symbol)
            else:
                flagLL = False
        else:
            production.set_first(diccFirst[symbol])
            if symbol not in diccFirst[production.get_production_symbol()]:
                diccFirst[production.get_production_symbol()].extend(diccFirst[symbol])
                diccFirst[production.get_production_symbol()] = list(set(diccFirst[production.get_production_symbol()]))
    return flagLL

def follow(diccFollow,nonTerminal):
    for i in range(len(rules)):
        if nonTerminal in rules[i].get_production():
            positionNonTerminal = rules[i].get_production().index(nonTerminal)
            if positionNonTerminal == len(rules[i].get_production())-1:
                if rules[i].get_production_symbol() == nonTerminal:
                    diccFollow[nonTerminal].extend(diccFollow[rules[i].get_production_symbol()])
                elif diccFollow[rules[i].get_production_symbol()] != [] and diccFollow[rules[i].get_production_symbol()] != ["$"]:
                    diccFollow[nonTerminal].extend(diccFollow[rules[i].get_production_symbol()])
                elif rules[i].get_production_symbol() != nonTerminal:
                    diccFollow[nonTerminal].extend(follow(diccFollow, rules[i].get_production_symbol()))
                diccFollow[nonTerminal] = list(set(diccFollow[nonTerminal]))
            elif rules[i].get_production()[positionNonTerminal+1] in terminals:
                diccFollow[nonTerminal].append(rules[i].get_production()[positionNonTerminal+1])
                diccFollow[nonTerminal] = list(set(diccFollow[nonTerminal]))
            else:
                firstNext = diccFirst[rules[i].get_production()[positionNonTerminal+1]].copy()
                if "e" in firstNext:
                    firstNext.remove("e")
                    if diccFollow[rules[i].get_production()[positionNonTerminal+1]] != []:
                        firstNext.extend(diccFollow[rules[i].get_production()[positionNonTerminal+1]])
                    else:
                        firstNext.extend(follow(diccFollow, rules[i].get_production()[positionNonTerminal+1]))
                diccFollow[nonTerminal].extend(firstNext)
                diccFollow[nonTerminal] = list(set(diccFollow[nonTerminal]))
    return diccFollow[nonTerminal]

def LLTableConstruction(diccFirst, diccFollow,rule):
    # Implementación de la función para construir la tabla LL(1)
    if "e" in rule.get_first():
        for i in range(len(diccFollow[rule.get_production_symbol()])):
            parsingTableLL[(rule.get_production_symbol(), diccFollow[rule.get_production_symbol()][i])] = rule.get_production()
    else:
        for i in range(len(rule.get_first())):
            parsingTableLL[(rule.get_production_symbol(), rule.get_first()[i])] = rule.get_production()

def searchRules(rules, symbol):
    listReturn = []
    for i in rules:
        if i.get_production_symbol() == symbol:
            x = Rule(symbol,"."+i.get_production())
            if x.get_production()[1] in nonTerminals:
                listReturn.append(x)
                if i.get_production()[0] != symbol:
                    listReturn.extend(searchRules(rules, x.get_production()[1]))
            else:
                listReturn.append(x)
    return listReturn

def movedot(rule):
    listrules = []
    production = rule.get_production()
    dotPosition = rule.get_production().index(".")
    newProduction = production[:dotPosition] + production[dotPosition+1] + "." + production[dotPosition+2:]
    try:
        dotPosition = newProduction.index(".")
        newSymbol = newProduction[dotPosition + 1]
        if newSymbol in nonTerminals:
            listrules.extend(searchRules(rules,newSymbol))
    except ValueError:
        newSymbol = None
    except IndexError:
        newSymbol = None
    newRule = Rule(rule.get_production_symbol(),newProduction)
    listrules.append(newRule)
    return listrules

def identify_dot(productions, symbolTransition):
    rulesRight = []
    for i in productions:
        positionNonTerminal = i.get_production().index(".")
        if positionNonTerminal < len(i.get_production())-1:
            if i.get_production()[positionNonTerminal+1] == symbolTransition:
                rulesRight.append(i)
    for i in rulesRight:
        productions.remove(i)
    return rulesRight

def createStateSRL(state):
    global numberState
    stackStates = []
    stackStates.append(state)
    i = 0
    SLRStates = []
    while not stackStates == []:
        stateActual = stackStates.pop(0)
        productions = stateActual.get_set_rules().copy()
        while i < len(productions):
            dotPosition = productions[i].get_production().index(".")
            if dotPosition == len(productions[i].get_production())-1:
                productions.remove(productions[i])
            else:
                symbolTransition = productions[i].get_production()[dotPosition+1]
                listnext = identify_dot(productions,symbolTransition)
                movedDots = []
                rulesMoved = []
                for pm in range(len(listnext)):
                    movedDots.extend(movedot(listnext[pm]))
                for j in movedDots:
                    rulesMoved.append([j.get_production_symbol(),j.get_production()])
                if symbolTransition == "e":
                    for k in rules:
                        if symbolTransition == k.get_production():
                            for l in diccFollow[k.get_production_symbol()]:
                                if (stateActual.get_number_state(), l) not in parsingTableSLR:
                                    parsingTableSLR[(stateActual.get_number_state(),l)] = f"r{rules.index(k)}"
                if  any(set(tuple(r) for r in rulesMoved) == set(tuple(r) for r in movement[1]) for movement in movementsCompleted):
                    for movement in movementsCompleted:
                        if set(tuple(r) for r in rulesMoved) == set(tuple(r) for r in movement[1]):
                            numberStatePrevious = movement[0]
                            break
                    if symbolTransition in nonTerminals:
                        parsingTableSLR[(stateActual.get_number_state(), symbolTransition)] = numberStatePrevious
                    else:
                        parsingTableSLR[(stateActual.get_number_state(), symbolTransition)] = f"d{numberStatePrevious}"
                else:
                    newState = State(numberState,movedDots)
                    movementsCompleted.append([numberState,rulesMoved])
                    newState.set_previus_state(stateActual.get_number_state())
                    newState.set_symbol(symbolTransition)
                    SLRStates.append(newState)
                    stackStates.append(newState)
                    numberState+=1
    return SLRStates

def printStates(listStatesResultant,size):
    for i in listStatesResultant[:size]:
        print(f"State {i.get_number_state()}: {i.get_previus_state()} -> {i.get_symbol()}")
        for j in i.get_set_rules():
            print(j.get_production_symbol(),"->",j.get_production())

def SLRTableConstruction(diccFollow, listStatesResultant):
    global flagSLR
    for i in listStatesResultant:
        if i.get_symbol() in nonTerminals:
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
            if j.get_production()[-1] == ".":
                ruleFinal = j.get_production().rstrip(".")
                for k in rules:
                    if ruleFinal == k.get_production():
                        for l in diccFollow[k.get_production_symbol()]:
                            if (i.get_number_state(), l) not in parsingTableSLR:
                                parsingTableSLR[(i.get_number_state(),l)] = f"r{rules.index(k)}"
                            else:
                                print(f"Ambiguity in the State {i.get_number_state()} with the rule {k.get_production_symbol()} -> {k.get_production()}")
                                flagSLR = False

def createHistoriesSLR(actionSymbol,stackSLRSymbol,inputSymbol,simbolsSymbol):
    actionHistory.append(actionSymbol)
    symbolHistory.append(list(simbolsSymbol))
    inputHistory.append(inputSymbol)
    stackSLRHistory.append(list(stackSLRSymbol))

def processSLR (string,stackSLR,processedSymbols,flagProcessSLR):
    if stackSLR[-1] == 1 and string == "$":
        flagProcessSLR = True
        return flagProcessSLR
    try:
        action = parsingTableSLR[stackSLR[-1],string[0]]
    except KeyError:
        return flagProcessSLR
    
    if action[0] == "d":
            processedSymbols.append(string[0])
            newString = string[1:]
            stackSLR.append(int(action[1:]))
            createHistoriesSLR(action,stackSLR,newString,processedSymbols)
            return processSLR(newString,stackSLR,processedSymbols,flagProcessSLR)
    
    if action[0] == "r":
        ruleReducce = rules[int(action[1])]
        if ruleReducce.get_production() == "e":
            processedSymbols.append(ruleReducce.get_production_symbol())
            try:
                stackSLR.append(parsingTableSLR[stackSLR[-1],processedSymbols[-1]])
                createHistoriesSLR(action,stackSLR,string,processedSymbols)
                return processSLR(string,stackSLR,processedSymbols,flagProcessSLR)
            except KeyError:
                return flagProcessSLR
        else:
            lengthRule = len(ruleReducce.get_production())
            if len(processedSymbols) == lengthRule:
                processedSymbols.clear()
            else:
                processedSymbols = processedSymbols[:(len(processedSymbols)-lengthRule)]
            processedSymbols.append(ruleReducce.get_production_symbol())
            newString = string
            stackSLR = stackSLR[:(len(stackSLR)-lengthRule)]
            try:
                stackSLR.append(parsingTableSLR[stackSLR[-1],processedSymbols[-1]])
            except KeyError:
                return flagProcessSLR
            createHistoriesSLR(action,stackSLR,newString,processedSymbols)
        return processSLR(newString,stackSLR,processedSymbols,flagProcessSLR)

def createHistoriesLL(stackSLRSymbol,inputSymbol):
    inputHistory.append(inputSymbol)
    stackSLRHistory.append(list(stackSLRSymbol))

def processLL(string,flagProcessLL):
    if stackLL[-1] == "$" and string == "$":
        stackLL.pop(0)
        createHistoriesLL(stackLL,string)
        flagProcessLL = True
        return flagProcessLL
    if stackLL[-1] == string[0]:
        string = string[1:]
        stackLL.pop(-1)
        createHistoriesLL(stackLL,string)
        return processLL(string,flagProcessLL)
    else:
        try:
            addStack = parsingTableLL[stackLL[-1],string[0]]
        except KeyError:
            return flagProcessLL
        stackLL.pop(-1)
        addStack=addStack[::-1]
        stackLL.extend(addStack)
        if addStack[-1] == "e":
            stackLL.pop(-1)
            createHistoriesLL(stackLL,string)
            return processLL(string,flagProcessLL)
        else:
            createHistoriesLL(stackLL,string)
            return processLL(string,flagProcessLL)

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

def print_parsing_process_SLR(stackSLRHistory, inputHistory, actionHistory,resutlSLR):
    #Crear DataFrame
    df = pd.DataFrame({"Stack": [" ".join(str(stack)) for stack in stackSLRHistory],
    "Input": [" ".join(cadena) for cadena in inputHistory],
    "Action": [" ".join(cadena) for cadena in actionHistory]})
    #Reemplazar celdas vacías con '-'
    df.replace('', '-', inplace=True)
    if resutlSLR:
        resultado = "Cadena aceptada"
    else:
        resultado = "Cadena rechazada"
    df.loc[len(df.index)] = [resultado, "-----","-----"]
    print(df.to_markdown(tablefmt="grid"))

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
flagProcessSLR = False

#Definition of variables to make the LL(1)
stackLL = ["$"]
flagLL= True
parsingTableLL = {}
flagProcessLL = False

with open("input.txt", "r") as file:
    num_rules = int(file.readline().strip())
    for i in range(num_rules):
        rule = file.readline().strip()
        parts = rule.split("->")
        if len(parts) == 2:
            parts = [parte.strip() for parte in parts]
        else:
            print("Does not meet the requirements of the txt file")
        parts[1] = parts[1].split(" ")
        if i == 0:
            startSymbolGrammar = parts[0]
        for j in range(len(parts[1])):
            identify_terminal(parts[0])
            identify_terminal(parts[1][j])
            rule = Rule(parts[0], parts[1][j])
            rules.append(rule)

    for line in file:
        line = line.strip()+"$"
        if line == "e$":
            break
        strings.append(line)

stackLL.append(startSymbolGrammar)
diccFirst = {}
diccFollow = {}
for i in range(len(nonTerminals)):
    diccFirst[nonTerminals[i]] = []
    diccFollow[nonTerminals[i]] = []
    if nonTerminals[i] == startSymbolGrammar:
        diccFollow[nonTerminals[i]].append("$")

for i in range (len(rules)-1,-1,-1):
    flagLL=first(rules[i],diccFirst,flagLL)

for symbol in nonTerminals:
    if diccFollow[symbol] == [] or diccFollow[symbol] == ["$"]:
        follow(diccFollow, symbol)

if not flagLL:
    print("No es LL(1)")
else:
    for i in nonTerminals:
        if "e" in diccFirst[i] and flagLL:
            for j in range(len(rules)):
                if rules[j].get_production_symbol() == i:
                    if rules[j].get_first() in diccFollow[i]:
                        flagLL= False
                        print("Ambiguity")
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
print("Rules:")
print_rules(rules)
print("----------------------------------------------------------------")

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
                else:
                    print("The string: ",i," not belongs to the grammar")
                print_parsing_process_LL(stackSLRHistory, inputHistory, resultLL)
                stackLL = ["$",startSymbolGrammar]
                inputHistory = []
                stackSLRHistory = []
        case "B":
            print("Tabla SLR(1):")
            print_parsing_table(parsingTableSLR)
            for i in strings:
                result = processSLR(i,stackSLR,processedSymbols,flagProcessSLR)
                if result:
                    print("The string: ",i," belongs to the grammar")
                else:
                    print("The string: ",i," not belongs to the grammar")
                print_parsing_process_SLR(stackSLRHistory, inputHistory, actionHistory, result)
                stackSLR = [0]
                inputHistory = []
                stackSLRHistory = []
                actionHistory = []
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
        else:
            print("The string: ",i," not belongs to the grammar")
        print_parsing_process_LL(stackSLRHistory, inputHistory, resultLL)
        stackLL = ["$",startSymbolGrammar]
        inputHistory = []
        stackSLRHistory = []
elif flagSLR:
    print("Grammar is SLR(1).")
    print("Tabla SLR(1):")
    print_parsing_table(parsingTableSLR)
    for i in strings:
        result = processSLR(i,stackSLR,processedSymbols,flagProcessSLR)
        if result:
            print("The string: ",i," belongs to the grammar")
        else:
            print("The string: ",i," not belongs to the grammar")
        print_parsing_process_SLR(stackSLRHistory, inputHistory, actionHistory, result)
        stackSLR = [0]
        inputHistory = []
        stackSLRHistory = []
        actionHistory = []
else:
    print("Grammar is neither LL(1) nor SLR(1).")