# Creamos el tablero de 10x10 con los íconos correspondientes
tabla = [
    ["◻️"] * 10 for _ in range(10)
]

# Posiciones iniciales del ratón y el gato
tabla[3][0] = "🐭"  # Ratón en fila 3, columna 0
tabla[8][9] = "🐱"  # Gato en fila 8, columna 9

gato = "🐱"
raton = "🐭"

# Posiciones actuales (coordenadas) de cada personaje
lugar_gato = [8, 9]
lugar_raton = [3, 0]

# Mostrar el tablero actual
def imprimir_tabla():
    for fila in tabla:
        print(" ".join(fila))
    print(" ")

# Movimientos del jugador (ratón solamente)
def mover_izq():
    if lugar_raton[1] > 0: #si no esta en la col 0
        tabla[lugar_raton[0]][lugar_raton[1]] = "◻️"
        lugar_raton[1] -= 1
        tabla[lugar_raton[0]][lugar_raton[1]] = "🐭"
    imprimir_tabla()
    print("mover izq")

def mover_abajo():
    if lugar_raton[0] < 9: #si no esta en la fila 9
        tabla[lugar_raton[0]][lugar_raton[1]] = "◻️"
        lugar_raton[0] += 1
        tabla[lugar_raton[0]][lugar_raton[1]] = "🐭"
    imprimir_tabla()
    print("mover abajo")

def mover_der():
    if lugar_raton[1] < 9:
        tabla[lugar_raton[0]][lugar_raton[1]] = "◻️"
        lugar_raton[1] += 1
        tabla[lugar_raton[0]][lugar_raton[1]] = "🐭"
    imprimir_tabla()
    print("mover der")

def mover_arriba():
    if lugar_raton[0] > 0:
        tabla[lugar_raton[0]][lugar_raton[1]] = "◻️"
        lugar_raton[0] -= 1
        tabla[lugar_raton[0]][lugar_raton[1]] = "🐭"
    imprimir_tabla()
    print("mover arriba")

# Definimos movimientos posibles del gato  #MOVIMIENTOS VALIDOS 
def movimientos_gato(pos_gato):
    fila, col = pos_gato
    movimientos = []
    if fila > 0: # Si no está en la fila 0, entonces puede moverse para arriba 
        movimientos.append([fila - 1, col])  # arriba
    if fila < 9:
        movimientos.append([fila + 1, col])  # abajo
    if col > 0:
        movimientos.append([fila, col - 1])  # izquierda
    if col < 9:
        movimientos.append([fila, col + 1])  # derecha
    return movimientos

def movimientos_raton(pos_raton):
    fila, col = pos_raton
    movimientos = []
    if fila > 0:
        movimientos.append([fila - 1, col])  # arriba
    if fila < 9:
        movimientos.append([fila + 1, col])  # abajo
    if col > 0:
        movimientos.append([fila, col - 1])  # izquierda
    if col < 9:
        movimientos.append([fila, col + 1])  # derecha
    return movimientos


# Función de evaluación simple: más cerca = mejor para el gato
def evaluar(pos_gato, pos_raton): 
    manhattan = abs(pos_gato[0] - pos_raton[0]) + abs(pos_gato[1] - pos_raton[1]) #distancia Manhattan
    return -manhattan

# Implementamos el Minimax SOLO para el gato 
def minimax(pos_gato, pos_raton, profundidad, maximizando): #Si ya no quedan turnos por simular (profundidad == 0) o el gato atrapó al ratón (pos_gato == pos_raton)
    if profundidad == 0 or pos_gato == pos_raton: #casos bases, con esto termina la recursividad
        return evaluar(pos_gato, pos_raton), pos_gato


    if maximizando:
        mejor_valor = float('-inf') #el mejro valor ahora es -infinito para poder comparar luego.
        mejor_mov = pos_gato #Guardamos la mejor jugada en mejor_mov qu es la pos actual del gato
        for mov in movimientos_gato(pos_gato): #recorre todas las jugadas posibles que el G puede hacer desde su posicion actual
            valor, _ = minimax(mov, pos_raton, profundidad - 1, False)
            # la _ "Solo me importa valor, ignoro el segundo valor."
            if valor > mejor_valor: #Si este movimiento da un mejor valor (más cerca del ratón), lo guardamos.
                mejor_valor = valor #distancia #actualiza el valor encontrado
                mejor_mov = mov #posicion #Guarda el movimiento que llevó a ese mejor valor
        return mejor_valor, mejor_mov #Al final devolvemos el mejor valor y la mejor jugada.
    else: #minimizando 
        mejor_valor = float('inf') #el ratón busca el valor más bajo posible para alejarse del gato
        mejor_mov = pos_raton #posicion actual del R como mejor mov
        for mov in movimientos_raton(pos_raton):
            valor, _ = minimax(pos_gato, mov, profundidad - 1, True) #si el raton se mueve ahi, que haria el gato?
            if valor < mejor_valor:  
                mejor_valor = valor  
                mejor_mov = mov 
        return mejor_valor, mejor_mov
   

# Mostramos tablero inicial
imprimir_tabla()

# Contador de movimientos del gato (máximo 15 turnos)
turno_gato = 0

# Bucle principal del juego
while True:
    # Turno del jugador (ratón)
    tecla = input("Tu turno (ratón): usa w/a/s/d para moverte o q para salir: ")# Lee lo que el jugador escribió (por teclado) y lo guarda en la variable tecla
    match tecla: # match sirve para tomar decisiones según el valor de una variable
        case "w": mover_arriba()
        case "a": mover_izq()
        case "s": mover_abajo()
        case "d": mover_der()
        case "q":
            print("Gracias por jugar :)")
            break
        case _:
            print("Presiona w, a, s, d")
            continue

    # Turno del GATO (IA con Minimax)
    
    valor, mejor_mov = minimax(lugar_gato, lugar_raton, 8, True) # acá se calcula el mejor movimiento para el gato, mirando hasta 8 turnos hacia adelante.
    tabla[lugar_gato[0]][lugar_gato[1]] = "◻️" # se actualiza el tablero para mover al gato a su nueva posición óptima.
    lugar_gato[0], lugar_gato[1] = mejor_mov
    tabla[lugar_gato[0]][lugar_gato[1]] = "🐱"
    
    imprimir_tabla()
    turno_gato += 1

    if lugar_gato == lugar_raton:
        print("¡El gato atrapó al ratón!")
        print(f"El gato ganó en {turno_gato} movimientos.")
        break

    if turno_gato >= 15:
        print("¡El ratón escapó exitosamente!")
        print("El ratón ganó porque el gato no lo atrapó en 15 movimientos.")
        break