"""
Universidad del Valle de Guatemala
Jorge Caballeros Pérez
Laboratorio A
Implementación de programa el cual recibe una ER y como resultado genera AFN con sus estados de aceptación y transiciones correspondientes.
"""

import graphviz
from collections import deque
from Regex import Regex as re


class AFN:
    def __init__(self, postfix):
        self.state_count = 0
        self.next_state = 1
        self.initial_state = ''
        self.final_state = ''
        self.operators = ['+', '-', '*', '/', '(', ')', '^', '$', '?']
        self.postfix = postfix
        self.result = self.createAFN(postfix)

    def concat(self, afn1, afn2):

        new_afn = []

        if type(afn1) == dict and type(afn2) == dict:
            self.state_count += 1
            self.next_state += 1
            afn2['state'] = afn1['next_state']
            afn2['next_state'] = f'S{self.next_state}'
            new_afn.append(afn1)
            new_afn.append(afn2)
            self.initial_state = afn1['state']
            self.final_state = afn2['next_state']

        elif type(afn2) == list and type(afn1) == dict:
            self.state_count += 1
            self.next_state += 1
            # changing next state of prev concatenaded afn
            afn1['state'] = f'S{self.state_count}'
            afn2[-1]['next_state'] = afn1['state']
            afn1['next_state'] = f'S{self.next_state}'
            self.final_state = afn1['next_state']
            afn2.append(afn1)
            new_afn = afn2.copy()
        print(new_afn)
        return new_afn

    def createAFN(self, postfix):
        stack = []

        for symbol in postfix:
            # hadle simple afn
            if symbol not in self.operators and symbol.isalpha() or symbol.isnumeric():
                simple_afn = {'state': f'S{self.state_count}',
                              'symbol': symbol, 'next_state': f'S{self.next_state}'
                              }
                stack.append(simple_afn)

            # Concatenación
            elif symbol == '$':
                afn1 = stack.pop()
                afn2 = stack.pop()
                new_afn = self.concat(afn1, afn2)
                stack.append(new_afn)

            elif symbol == '*':  # Kleene
                break

            elif symbol == '|':  # Union
                break
            elif symbol == ' ε ':  # Epsilon
                break
            elif symbol == '?':  # Opcional
                break
        return stack


regex = re('a$b$c$d')
print(regex.postfix)
nfa = AFN(regex.postfix)
