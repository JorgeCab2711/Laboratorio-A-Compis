"""
Universidad del Valle de Guatemala
Jorge Caballeros Pérez
Laboratorio A
Implementación de programa el cual recibe una ER y como resultado genera AFN con sus estados de aceptación y transiciones correspondientes.
"""

import graphviz
from collections import deque
from Regex import Regex as re
from Node import Node 


class AFN:
    def __init__(self, postfix):
        self.operators = ['+', '-', '*', '/', '(', ')', '^','%', '?']
        self.postfix = postfix
        self.result = self.createAFN(postfix)
        self.initial_state = self.result[0]['state']
        self.final_state = self.result[-1]['state']
        
    def concat(self, afn1, afn2):
        
        new_afn = []
        afn2['state'] = afn1['next_state']
        afn2['next_state'] = 'Final'
        new_afn.append(afn1)
        new_afn.append(afn2)
        self.final_state = afn2['state']
        self.initial_state = afn1['state']
        
        
        
        
    
    def createAFN(self, postfix):
        stack = []
        state_count = 0
        next_state = 1
        for symbol in postfix:
            if symbol not in self.operators and symbol.isalpha() or symbol.isnumeric(): #habdle simple afn
                simple_afn = {'state': f'S{state_count}','symbol':symbol, 'next_state': f'S{next_state}'}
                stack.append(simple_afn)
            elif symbol == '*': #Kleene
                break
            elif symbol == '%': #Concatenación
                self.concat(stack[-2],stack[-1])
            elif symbol == '|': #Union
                break
            elif symbol == ' ε ': #Epsilon
                break
            elif symbol == '?': #Opcional
                break
        return stack
    
    
                
        
        



regex = re('a%b')
nfa = AFN(regex.postfix)

# print(f"Infix: {regex.infix}\nPostfix: {regex.postfix}")

