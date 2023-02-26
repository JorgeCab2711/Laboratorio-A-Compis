"""
Universidad del Valle de Guatemala
Jorge Caballeros Pérez
Laboratorio A
Implementación de programa el cual recibe una ER y como resultado genera AFN con sus estados de aceptación y transiciones correspondientes.
"""

import graphviz
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

class AFN:
    def __init__(self, alphabet, postfix):
        self.alphabet = alphabet
        self.postfix = postfix
        self.states = set()
        self.transitions = []
        self.start_state = None
        self.final_states = set()
        self.generate_afn()

    def generate_afn(self):
        stack = []
        for char in self.postfix:
            if char in self.alphabet:
                state1 = 'q' + str(len(self.states))
                state2 = 'q' + str(len(self.states) + 1)
                self.states.add(state1)
                self.states.add(state2)
                self.transitions.append((state1, char, state2))
                stack.append((state1, state2))
            elif char == '*':
                state1, state2 = stack.pop()
                self.transitions.append((state2, '', state1))
                self.transitions.append((state1, '', state2))
                self.states.add(state1)
                self.states.add(state2)
                stack.append((state1, state2))
            elif char == '%':
                state2, state2 = stack.pop()
                state1, state1 = stack.pop()
                self.transitions.append((state1, '', state2))
                self.states.add(state1)
                self.states.add(state2)
                stack.append((state1, state2))
            elif char == '|':
                state2, state2 = stack.pop()
                state1, state1 = stack.pop()
                new_start_state = 'q' + str(len(self.states))
                new_final_state = 'q' + str(len(self.states) + 1)
                self.states.add(new_start_state)
                self.states.add(new_final_state)
                self.transitions.append((new_start_state, '', state1))
                self.transitions.append((new_start_state, '', state2))
                self.transitions.append((state1, '', new_final_state))
                self.transitions.append((state2, '', new_final_state))
                stack.append((new_start_state, new_final_state))
        self.start_state, self.final_states = stack.pop()

    def to_graphviz(self):
        graph = graphviz.Digraph()
        graph.node(self.start_state, shape='point')
        for state in self.states:
            graph.node(state, shape='circle')
            if state in self.final_states:
                graph.attr('node', shape='doublecircle')
            else:
                graph.attr('node', shape='circle')
            for transition in self.transitions:
                if transition[0] == state:
                    label = transition[1] if transition[1] != '' else 'ε'
                    graph.edge(transition[0], transition[2], label=label)
        return graph


alfabeto = set('abcd')
regex = Regex('a+b')
print(f"Infix: {regex.infix}\nPostfix: {regex.postfix}")

afn = AFN(alfabeto, regex.postfix)

graph = afn.to_graphviz()

graph.view()