"""
Universidad del Valle de Guatemala
Jorge Caballeros Pérez
Laboratorio A
Implementación de programa el cual recibe una ER y como resultado genera AFN con sus estados de aceptación y transiciones correspondientes.
"""
from graphviz import Digraph

class Regex:
    def __init__(self, regex) -> None:
        self.infix = regex
        self.postfix = self.infix_to_postfix()
        self.postfixLists = self.listPostfix()
        
    def infix_to_postfix(self):
        infix =  self.infix
        # Asignar la precedencia de los operadores
        precedencia = {'?': 4,'*': 3, '+': 2, '~': 1}
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

    def listPostfix(self):
        return [i for i in self.postfix]
    
class State:
    """Representa un estado en un AFN."""
    def __init__(self, label=None, edges=None):
        self.label = label
        self.edges = edges or []

class NFA:
    """Representa un Autómata Finito No Determinístico."""
    def __init__(self, start=None, end=None):
        self.start = start
        self.end = end

    def concatenate(self, other):
        """Concatena este AFN con otro AFN."""
        self.end.edges.append(other.start)
        self.end = other.end

    def alternate(self, other):
        """Realiza la operación alternación en este AFN y otro AFN."""
        new_start = State()
        new_start.edges = [self.start, other.start]
        new_end = State()
        self.end.edges.append(new_end)
        other.end.edges.append(new_end)
        self.start, self.end = new_start, new_end

    def kleene_star(self):
        """Realiza la operación de cierre de Kleene en este AFN."""
        new_start, new_end = State(), State()
        new_start.edges = [self.start]
        self.end.edges.extend([self.start, new_end])
        self.start, self.end = new_start, new_end

def postfix_to_nfa(postfix):
    """Convierte una expresión regular en formato postfix a un AFN."""
    stack = []
    for char in postfix:
        if char == "%":
            second, first = stack.pop(), stack.pop()
            first.concatenate(second)
            stack.append(first)
        elif char == "|":
            second, first = stack.pop(), stack.pop()
            first.alternate(second)
            stack.append(first)
        elif char == "*":
            nfa = stack.pop()
            nfa.kleene_star()
            stack.append(nfa)
        else:
            state = State(label=char)
            nfa = NFA(start=state, end=state)
            stack.append(nfa)
    return stack.pop()

def visualize_nfa(nfa):
    """Visualiza un AFN utilizando Graphviz."""
    graph = Digraph()
    nodes, edges = set(), set()
    start, end = nfa.start, nfa.end
    nodes.update([start, end])
    for current in nodes:
        if current == end:
            graph.node(str(current.label), shape='doublecircle')
        else:
            graph.node(str(current.label), shape='circle')
        for edge in current.edges:
            nodes.add(edge)
            edges.add((current, edge))
    for start, end in edges:
        graph.edge(str(start.label), str(end.label), label='ε')
    return graph

regex = Regex('a?b')
postfix = regex.postfix
nfa = postfix_to_nfa(postfix)
print(f"Postfix: {postfix}")

graph = visualize_nfa(nfa)
graph.render('nfa.gv', view=True)



