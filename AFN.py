"""
Universidad del Valle de Guatemala
Jorge Caballeros Pérez
Laboratorio A
Implementación de programa el cual recibe una ER y como resultado genera AFN con sus estados de aceptación y transiciones correspondientes.
"""
# Notes:
# - this code is not finished yet
# - you have to write the regex concatenation symbol as '$' and not as '.' because '.' is used for the dot operator
# - concatenation will not work with empty strings , you have to put the '$' symbol in between


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

    # method that concatenates two nfas
    def concat(self, afn1, afn2):
        new_afn = []

        if type(afn1) == dict and type(afn2) == dict:
            self.state_count += 1
            self.next_state += 1
            # update afn2's state to afn1's next_state
            afn1['state'] = afn2['next_state']
            afn1['next_state'] = f'S{self.next_state}'
            new_afn.append(afn2)
            new_afn.append(afn1)
            self.initial_state = afn2['state']
            self.final_state = afn1['next_state']

        elif type(afn2) == list and type(afn1) == dict:
            self.state_count += 1
            self.next_state += 1
            # changing next state of prev concatenated afn
            afn1_copy = afn1.copy()  # create a copy of afn1
            afn1_copy['state'] = f'S{self.state_count}'
            afn2[-1]['next_state'] = afn1_copy['state']
            afn1_copy['next_state'] = f'S{self.next_state}'
            self.final_state = afn1_copy['next_state']
            afn2.append(afn1_copy)
            new_afn = afn2.copy()
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
                print(f'Concatenación: {new_afn}')

            elif symbol == '*':  # Kleene
                break

            elif symbol == '|':  # Union
                break
            elif symbol == ' ε ':  # Epsilon
                break
            elif symbol == '?':  # Opcional
                break

        return stack


regex = re('(a$b)$(c$d)')
print(regex.postfix)
nfa = AFN(regex.postfix)
print(f"Initial state: {nfa.initial_state}\nFinal state: {nfa.final_state}")
print(f'Result: \n{nfa.result}')
