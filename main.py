from Rule import Rule


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
        print("Reduccion por la izquieda")
        flagLL = False
        print("Flag LL: ", flagLL)
        production.set_first(".")
    else:
        if simbolo in terminales:
            production.set_first(simbolo)
            if simbolo not in diccFirst[production.get_simbolo_produccion()]:
                diccFirst[production.get_simbolo_produccion()].append(simbolo)

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
                diccFollow[noTerminal].extend(diccFollow[reglas[i].get_simbolo_produccion()])
                diccFollow[noTerminal] = list(set(diccFollow[noTerminal]))
            elif reglas[i].get_produccion()[posicion+1] in terminales:
                diccFollow[noTerminal].append(reglas[i].get_produccion()[posicion+1])
                diccFollow[noTerminal] = list(set(diccFollow[noTerminal]))
            else:
                firstNext = diccFirst[reglas[i].get_produccion()[posicion+1]]
                if "e" in firstNext:
                    firstNext.remove("e")
                    if diccFollow[reglas[i].get_produccion()[posicion+1]] != []:
                        firstNext.extend(diccFollow[reglas[i].get_produccion()[posicion+1]])
                    else:
                        firstNext.extend(follow(diccFollow, reglas[i].get_produccion()[posicion+1]))
                diccFollow[noTerminal].extend(firstNext)
                diccFollow[noTerminal] = list(set(diccFollow[noTerminal]))
    return diccFollow[noTerminal]








reglas = []
strings = []
terminales = []
noTerminales = []
flagLL= True
flagSLR= True



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
        for i in range(len(partes[1])):
            identify_terminal(partes[1][i])
            rule = Rule(partes[0], partes[1][i])
            reglas.append(rule)


    # 3. Leer los strings hasta encontrar "e"
    for linea in archivo:
        linea = linea.strip()+"$"
        if linea == "e":
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


if(not flagLL):
    print("La gramatica no es LL(1)")
#Calcular los follow

for simbolo in noTerminales:
    if diccFollow[simbolo] == [] or diccFollow[simbolo] == ["$"]:
        #follow(diccFollow, simbolo)
        print()
    print(f"Simbolo de produccion: {simbolo}")
    print(f"First: {diccFirst[simbolo]}")
    print(f"Follow: {diccFollow[simbolo]}")
    print()





print("Terminales:")
print(terminales)
print("No terminales:")
print(noTerminales)
print("Diccionario FIRST:")
print(diccFirst)
print("Diccionario FOLLOW:")
print(diccFollow)
print("Flag LL:")
print(flagLL)