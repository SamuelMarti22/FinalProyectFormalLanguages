reglas = []
strings = []

with open("input.txt", "r") as archivo:
    # 1. Leer cuántas reglas hay
    num_reglas = int(archivo.readline().strip())

    # 2. Leer las reglas
    for _ in range(num_reglas):
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
        # Limpiar espacios en las reglas
        
        reglas.append(partes)

    # 3. Leer los strings hasta encontrar "e"
    for linea in archivo:
        linea = linea.strip()
        if linea == "e":
            break
        strings.append(linea)

# Mostrar para verificar
print("Reglas:")
print(reglas)
print("Strings:")
print(strings)
