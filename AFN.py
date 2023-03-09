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
from tabulate import tabulate


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
            afn1['next_state'] = [f'S{self.next_state}']
            new_afn.append(afn2)
            new_afn.append(afn1)

        elif type(afn2) == list and type(afn1) == dict:
            self.state_count += 1
            self.next_state += 1
            # changing next state of prev concatenated afn
            afn1_copy = afn1.copy()  # create a copy of afn1
            afn1_copy['state'] = f'S{self.state_count}'
            afn2[-1]['next_state'] = [afn1_copy['state']]
            afn1_copy['next_state'] = [f'S{self.next_state}']
            self.final_state = afn1_copy['next_state'][0]
            afn2.append(afn1_copy)
            new_afn = afn2.copy()
        # Debug the states that are being changed to lists
        for i in new_afn:
            if type(i['state']) == list:
                i['state'] = i['state'][0]

        return new_afn



    # Method that applies the kleene star operator to an afn
    def kleene(self, afn):
        new_afn = []
        new_initial_state_afn = {'state': 'S-1',
                                 'symbol': 'ε',
                                 'next_state': [afn[0]['state']]
                                 }

        new_final_state_afn = {'state': afn[-1]['next_state'][0],
                               'symbol': 'ε',
                               'next_state': [afn[-1]['next_state'][0]]
                               }

        new_afn.append(afn)
        return new_afn

    # Method that applies the union operator to two afns
    def union(self, nfa2, nfa1):
        new_nfa = []

        if type(nfa1) is not list:
            nfa1 = [nfa1]
        if type(nfa2) is not list:
            nfa2 = [nfa2]

        

        new_initial_state = [{'state': 'S-1',
                             'symbol': 'ε',
                              'next_state': []
                              }]
        
        # new_initial_state[0]['next_state'].append(nfa1[0]['state'])
        # new_initial_state[0]['next_state'].append(nfa2[0]['state'])
        # new_nfa.append(new_initial_state)
        # new_nfa.append(nfa1)
        # new_nfa.append(nfa2)
        # print(self.state_count)
        print(nfa1)
        print(nfa2)
        
        new_final_state = [{'state': f'S{self.state_count}',
                            'symbol': 'ε',
                            'next_state': []
                            }]
        new_nfa.append(new_final_state)
        

        return new_nfa

    # Method that creates the afn from a postfix expression

    def createAFN(self, postfix):
        stack = []

        for symbol in postfix:
            # hadle simple afn
            if symbol not in self.operators and symbol.isalpha() or symbol.isnumeric():
                simple_afn = {'state': f'S{self.state_count}',
                              'symbol': symbol,
                              'next_state': [f'S{self.next_state}']
                              }
                stack.append(simple_afn)

                

            # Concatenación
            elif symbol == '$':
                afn1 = stack.pop()
                afn2 = stack.pop()
                new_afn = self.concat(afn1, afn2)
                stack.append(new_afn)

            # Union
            elif symbol == '|':
                afn1 = stack.pop()
                afn2 = stack.pop()
                new_afn = self.union(afn1, afn2)
                stack.append(new_afn)

            # Kleene
            elif symbol == '*':
                pass
            # Epsilon
            elif symbol == ' ε ':
                break
            # Opcional
            elif symbol == '?':
                break

        # TODO set initial and final states
        # self.initial_state = stack[0][0]['state']
        # self.final_state = stack[0][-1]['state']
        return stack

    def graphNFA(self, nfa):

        dot = graphviz.Digraph(comment='NFA')

        if type(nfa[0]) is not dict:
            nfa = nfa[0]

        # Add the nodes to the graph
        for transition in nfa:
            dot.node(transition['state'], shape='circle')

        # Add the transitions to the graph
        for transition in nfa:
            for next_state in transition['next_state']:
                dot.edge(transition['state'], next_state,
                         label=transition['symbol'])

        # Set the start state
        dot.attr('node', shape='point')
        dot.edge('', nfa[0]['state'])

        # Set the final state
        dot.attr('node', shape='doublecircle')
        dot.node(nfa[-1]['next_state'][-1], shape='doublecircle')

        return dot


regex = re('(a|b)')
print(regex.postfix)
nfa = AFN(regex.postfix)
# print(f"Initial state: {nfa.initial_state}\nFinal state: {nfa.final_state}")
print(f'Result:\n')
headers = ['State', 'Symbol', 'Next State']
rows = []

for i in range(len(nfa.result)):
    for j in range(len(nfa.result[i])):
        for k in range(len(nfa.result[i][j])):
            state = nfa.result[i][j][k]['state']
            symbol = nfa.result[i][j][k]['symbol']
            next_state = ', '.join(nfa.result[i][j][k]['next_state'])
            rows.append([state, symbol, next_state])

# Use the tabulate module to create a formatted table
table = tabulate(rows, headers=headers)

# Print the table
print(table)

# dot = nfa.graphNFA(nfa.result[0])
# dot.render('nfa', format='pdf', view=True)
