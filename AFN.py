"""
Universidad del Valle de Guatemala
Jorge Caballeros Pérez
Laboratorio A
Implementación de programa el cual recibe una ER y como resultado genera AFN con sus estados de aceptación y transiciones correspondientes.
"""
import re
from graphviz import Digraph
from collections import deque


class Regex:
    def __init__(self, regex) -> None:
        self.infix = regex
        self.postfix = self.infixToPostfix(self.infix)
        self.postfixLists = self.listPostfix()

    def infixToPostfix(self, expression):

        Operators = set(['+', '-', '*', '/', '(', ')', '^'])

        Priority = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}

        stack = []

        output = ''

        for character in expression:

            if character not in Operators:

                output += character

            elif character == '(':

                stack.append('(')

            elif character == ')':

                while stack and stack[-1] != '(':

                    output += stack.pop()

                stack.pop()

            else:

                while stack and stack[-1] != '(' and Priority[character] <= Priority[stack[-1]]:

                    output += stack.pop()

                stack.append(character)

        while stack:

            output += stack.pop()

        return output

    # Función que convierte una expresión regular en formato postfix a una lista.

    def listPostfix(self):
        return [i for i in self.postfix]


class State:
    """Representa un estado en un AFN."""

    def __init__(self, label=None, edges=None):
        self.label = label
        self.edges = edges or []


class NFA:
    def __init__(self, postfix) -> None:
        self.postFix = postfix


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


regex = Regex('ab|*cd.|')
print(f"Infix: {regex.infix}\nPostfix: {regex.postfix}")
nfa = NFA.postfix_to_nfa(regex.postfix)
nfa.render('nfa')
