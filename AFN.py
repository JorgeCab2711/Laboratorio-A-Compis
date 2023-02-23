"""
Universidad del Valle de Guatemala
Jorge Caballeros Pérez
Laboratorio A
Implementación de programa el cual recibe una ER y como resultado genera AFN con sus estados de aceptación y transiciones correspondientes.
"""
import graphviz


class Estado:
    def __init__(self, transiciones=None, aceptacion=False):
        if transiciones is None:
            transiciones = {}
        self.transiciones = transiciones
        self.aceptacion = aceptacion


class AFN:
    def __init__(self, inicio, fin):
        self.estados = {inicio, fin}
        self.inicio = inicio
        self.fin = fin
        self.transiciones = {}

    def agregar_transicion(self, origen, simbolo, destino):
        if origen not in self.estados:
            raise ValueError('El estado de origen no pertenece al AFN')
        if destino not in self.estados:
            raise ValueError('El estado de destino no pertenece al AFN')
        if (origen, simbolo) in self.transiciones:
            raise ValueError('La transición ya existe')
        self.transiciones[(origen, simbolo)] = destino


def infix_to_postfix(infix):
    # Asignar la precedencia de los operadores
    precedencia = {'*': 3, '+': 2, '.': 1}
    # Inicializar una pila para los operadores y una lista para la salida
    operadores = []
    salida = []
    # Separar la expresión en una lista de tokens
    tokens = list(infix)
    # Inicializar un contador de paréntesis
    contador_parentesis = 0
    # Iterar sobre cada token en la lista
    for token in tokens:
        # Si el token es un operando, añadirlo a la salida
        if token.isalnum():
            salida.append(token)
        # Si el token es un operador
        elif token in precedencia:
            # Mientras haya operadores en la pila y el operador en la cima tenga mayor precedencia
            while operadores and operadores[-1] != '(' and precedencia[operadores[-1]] >= precedencia[token]:
                # Añadir el operador de la cima de la pila a la salida
                salida.append(operadores.pop())
            # Añadir el operador a la pila
            operadores.append(token)
        # Si el token es un paréntesis de apertura
        elif token == '(':
            # Añadirlo a la pila de operadores
            operadores.append(token)
            # Incrementar el contador de paréntesis
            contador_parentesis += 1
        # Si el token es un paréntesis de cierre
        elif token == ')':
            # Si hay un paréntesis de apertura correspondiente en la pila de operadores
            if '(' in operadores:
                # Mientras no se encuentre un paréntesis de apertura en la pila de operadores
                while operadores and operadores[-1] != '(':
                    # Añadir el operador de la cima de la pila a la salida
                    salida.append(operadores.pop())
                # Remover el paréntesis de apertura de la pila de operadores
                operadores.pop()
                # Decrementar el contador de paréntesis
                contador_parentesis -= 1
            # Si no hay un paréntesis de apertura correspondiente, lanzar una excepción
            else:
                raise ValueError('Los paréntesis no están balanceados')
    # Si el contador de paréntesis no es cero, lanzar una excepción
    if contador_parentesis != 0:
        raise ValueError('Los paréntesis no están balanceados')
    # Mientras queden operadores en la pila, añadirlos a la salida
    while operadores:
        salida.append(operadores.pop())
    # Unir la lista de salida en una cadena y devolverla
    return ''.join(salida)


def postfix_to_afn(postfix):
    # Definir la clase Nodo para representar los estados del AFN
    class Nodo:
        def __init__(self, simbolo=None):
            self.simbolo = simbolo
            self.primeros = set()
            self.ultimos = set()
            self.transiciones = {}

    # Definir la función para unir dos AFN
    def union(afn1, afn2):
        # Crear el nuevo estado inicial y final
        inicio = Nodo()
        fin = Nodo()
        # Agregar transiciones vacías del nuevo estado inicial a los estados iniciales de los AFN originales
        inicio.transiciones[''] = [afn1[0], afn2[0]]
        # Agregar transiciones vacías de los estados finales de los AFN originales al nuevo estado final
        afn1[1].transiciones[''] = [fin]
        afn2[1].transiciones[''] = [fin]
        # Actualizar los conjuntos de primeros y últimos del nuevo estado inicial y final
        inicio.primeros = afn1[0].primeros.union(afn2[0].primeros)
        fin.ultimos = afn1[1].ultimos.union(afn2[1].ultimos)
        # Devolver el nuevo AFN
        return [inicio, fin]

    # Definir la función para concatenar dos AFN
    def concatenacion(afn1, afn2):
        # Agregar transiciones vacías del estado final del primer AFN al estado inicial del segundo AFN
        afn1[1].transiciones[''] = [afn2[0]]
        # Actualizar los conjuntos de primeros y últimos del estado inicial y final del nuevo AFN
        inicio = afn1[0]
        fin = afn2[1]
        inicio.primeros = afn1[0].primeros
        fin.ultimos = afn2[1].ultimos
        # Devolver el nuevo AFN
        return [inicio, fin]

    # Definir la función para aplicar el operador de cerradura de Kleene a un AFN
    def cerradura(afn):
        # Crear el nuevo estado inicial y final
        inicio = Nodo()
        fin = Nodo()
        # Agregar transiciones vacías del nuevo estado inicial a los estados inicial y final del AFN original
        inicio.transiciones[''] = [afn[0], fin]
        afn[1].transiciones[''] = [afn[0], fin]
        # Actualizar los conjuntos de primeros y últimos del nuevo estado inicial y final
        inicio.primeros = afn[0].primeros
        fin.ultimos = afn[1].ultimos
        # Agregar transiciones vacías del estado final del AFN original a su estado inicial y al nuevo estado final
        afn[1].transiciones[''] = [afn[0], fin]
        # Devolver el nuevo AFN
        return [inicio, fin]

    # Definir la función para aplicar una operación a un AFN
    def aplicar_operacion(operacion, pila):
        if operacion == '|':
            afn2 = pila.pop()
            afn1 = pila.pop()
            pila.append(union(afn1, afn2))
        elif operacion == '.':
            afn2 = pila.pop()
            afn1 = pila.pop()
            pila.append(concatenacion(afn1, afn2))
        elif operacion == '*':
            afn = pila.pop()
            pila.append(cerradura(afn))

    # Definir la pila para almacenar los AFN
    pila = []
    # Iterar por cada símbolo de la expresión postfix
    for simbolo in postfix:
        if simbolo == '|':
            aplicar_operacion(simbolo, pila)
        elif simbolo == '.':
            aplicar_operacion(simbolo, pila)
        elif simbolo == '*':
            aplicar_operacion(simbolo, pila)
        else:
            # Crear un AFN para el símbolo y agregarlo a la pila
            inicio = Nodo()
            fin = Nodo()
            inicio.transiciones[simbolo] = [fin]
            inicio.primeros.add(inicio)
            fin.ultimos.add(fin)
            pila.append([inicio, fin])

    # Al finalizar, la pila debe tener un único AFN, que es el resultado final
    afn = pila.pop()

    # Crear el objeto Digraph de Graphviz
    dot = graphviz.Digraph()
    dot.attr(rankdir='LR')

    # Definir un diccionario para mapear cada estado del AFN a un nombre
    nombres_estados = {}
    for i, estado in enumerate(afn[0].primeros):
        nombres_estados[estado] = f'q{i}'

    # Definir una función auxiliar para agregar un estado al grafo
    def agregar_estado(estado):
        nombre = nombres_estados[estado]
        dot.node(nombre, nombre, shape='circle')
        if estado in afn[0].primeros:
            dot.node(nombre, nombre, shape='doublecircle')
        if estado in afn[1].ultimos:
            dot.node(nombre, nombre, shape='doublecircle')

    # Definir una función auxiliar para agregar una transición al grafo
    def agregar_transicion(estado_origen, estado_destino, simbolo):
        nombre_origen = nombres_estados[estado_origen]
        nombre_destino = nombres_estados[estado_destino]
        dot.edge(nombre_origen, nombre_destino, label=simbolo)

    # Iterar por cada estado del AFN y agregarlo al grafo
    for estado in afn[0].primeros:
        agregar_estado(estado)

    # Iterar por cada estado del AFN y agregar sus transiciones al grafo
    for origen, transiciones in afn[0].transiciones.items():
        for destino in transiciones:
            agregar_transicion(origen, destino, '')
    # Iterar por cada estado del AFN y agregar sus transiciones al grafo
    for estado in afn[0].primeros:
        for simbolo, transiciones in estado.transiciones.items():
            for destino in transiciones:
                agregar_transicion(estado, destino, simbolo)

    # Retornar el grafo
    return dot


def listPostfix(postfix):
    return [i for i in postfix]


regex = 'ab*'
postfix = infix_to_postfix(regex)
postfixList = listPostfix(postfix)
afn = postfix_to_afn(postfixList)
print(
    f'\n\nRegular expression: {regex}\n\nPostfix List: {postfixList}\nPostfix: {postfixList}\nAFN: {afn}')
