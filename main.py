from Rule import Rule
from State import State
import pandas as pd


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
    print("Diccionario")
    print(diccFirst)
    
    print("Calculando FIRST")
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
            print("Simbolo no terminal")
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
                if diccFollow[reglas[i].get_simbolo_produccion()] != [] and diccFollow[reglas[i].get_simbolo_produccion()] != ["$"]:
                    diccFollow[noTerminal].extend(diccFollow[reglas[i].get_simbolo_produccion()])
                else:
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
    for i in rules:
        listaReturn = []
        if i.get_simbolo_produccion() == symbol:
            x = Rule(symbol,"."+i.get_produccion())
            if x.get_produccion()[1] in noTerminales:
                listaReturn.append(x)
                listaReturn.extend(searchRules(rules, x.get_produccion()[1]))
                return listaReturn
            else:
                listaReturn.append(x)
                return listaReturn

def createStateSRL(state):
    
    # Implementación de la función para crear el estado SLR
    print("Aun no, ahorita mañana")

def construccionTablaSLR(diccFollow, regla):
    print("Aun no, ahorita mañana")

def print_parsing_table(parsingTableLL):
    # Filas y columnas
    filas = sorted({k[0] for k in parsingTableLL})
    columnas = sorted({k[1] for k in parsingTableLL})

    # Crear DataFrame
    df = pd.DataFrame('', index=filas, columns=columnas)
    for (fila, col), valor in parsingTableLL.items():
        df.at[fila, col] = valor

    # Reemplazar celdas vacías con '-'
    df.replace('', '-', inplace=True)

    # Imprimir con líneas
    print(df.to_markdown(tablefmt="grid"))

reglas = []
strings = []
terminales = []
noTerminales = []
flagLL= True
flagSLR= True
parsingTableLL = {}
parsingTableSLR = {}

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
    print(f"Simbolo de produccion: {reglas[i].get_simbolo_produccion()}")
    print(f"Produccion: {reglas[i].get_produccion()}")
    print(f"First: {reglas[i].get_first()}")
    print()


for simbolo in noTerminales:
    if diccFollow[simbolo] == [] or diccFollow[simbolo] == ["$"]:
        follow(diccFollow, simbolo)
        print()
    print(f"Simbolo de produccion: {simbolo}")
    print(f"First: {diccFirst[simbolo]}")
    print(f"Follow: {diccFollow[simbolo]}")
    print()

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
    print("Construir table")
    for i in range(len(reglas)):
        construccionTablaLL(diccFirst,diccFollow,reglas[i])

reglaInicial = Rule(primero+"'","."+primero)
inicial = State(0,[reglaInicial])

hola = searchRules(reglas, primero)

for i in hola:
    print(f"Simbolo de produccion: {i.get_simbolo_produccion()}")
    print(f"Produccion: {i.get_produccion()}")

print()

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