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
        # TODO: fix the initial and final states
        # self.initial_state = self.result[0][0]['state']
        # self.final_state = self.result[0][-1]['state']

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

        new_afn = self.normilizeNFADataType(new_afn)
        self.state_count = len(new_afn)
        self.next_state = self.state_count + 1
        self.normilizeConcatNames(new_afn)

        return new_afn

    # Method that applies the union operator to two afns

    def union(self, nfa2, nfa1):
        new_nfa = []

        if type(nfa1) is not list:
            nfa1 = [nfa1]
        if type(nfa2) is not list:
            nfa2 = [nfa2]
        
        
        # New initial state for the new nfa
        initial_state = {'state': 'S-1',
                         'symbol': 'ε',
                         'next_state': [nfa1[0]['state'], nfa2[0]['state']]
                         }
        
        # Epsilon state nfa 1
        new_state_nfa1 = {'state': f'S{self.state_count}',
                          'symbol': 'ε',
                          'next_state': []
                          }
        self.state_count += 1
        self.next_state += 1

        # Epsilon state nfa 2
        new_state_nfa2 = {'state': f'S{self.state_count}',
                          'symbol': 'ε',
                          'next_state': []
                          }

        self.state_count += 1
        self.next_state += 1

        nfa1[-1]['next_state'] = [new_state_nfa1['state']]
        nfa2[-1]['next_state'] = [new_state_nfa2['state']]

        final_state = {'state': 'Sn',
                       'symbol': '',
                       'next_state': []
                       }

        new_state_nfa1['next_state'] = [final_state['state']]
        new_state_nfa2['next_state'] = [final_state['state']]

        nfa1.append(new_state_nfa1)
        nfa2.append(new_state_nfa2)
                
        
        new_nfa.append(initial_state)
        new_nfa.extend(nfa2)
        new_nfa.extend(nfa1)

        new_nfa = self.normilizeNFADataType(new_nfa)
        new_nfa = self.checkCoherence(new_nfa)
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
                self.state_count += 1
                self.next_state += 1
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
            # Opcional
            elif symbol == '?':
                break
        return stack

    def graphNFA(self, nfa):
        dot = graphviz.Digraph(comment='NFA', graph_attr={'rankdir': 'LR'})
        try:
            print(type(nfa[0]) != list)
        except:
            nfa = [nfa]

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

    def normilizeNFADataType(self, nfa):
        dict_list = []
        for element in nfa:
            if isinstance(element, dict):
                dict_list.append(element)
            elif isinstance(element, list):
                for subelement in element:
                    if isinstance(subelement, dict):
                        dict_list.append(subelement)

        return dict_list

    def normilizeConcatNames(self, nfa):
        counter = 0
        for j in nfa:
            j['state'] = f'S{counter}'
            j['next_state'] = [f'S{counter+1}']
            counter += 1

    def checkCoherence(self, nfa):
        #removing the incoherence that the initial state has with itself
        for i in nfa:
            if i['state'] == 'S-1':
                for j in i['next_state']:
                    if j == 'S-1':
                        i['next_state'].remove(j)
                
            
        
                                
        return nfa
                        
                
        
            
            
        
            


regex = re('(a$b$c$d$f|c|e)')
print(regex.postfix)
nfa = AFN(regex.postfix)
print(f"Initial state: {nfa.initial_state}\nFinal state: {nfa.final_state}")
print(f'Result:\n')
# TODO : uncomment this to print the table
headers = ['State', 'Symbol', 'Next State']
rows = []
headers = nfa.result[0][0].keys()
rows = [d.values() for d in nfa.result[0]]
print(tabulate(rows, headers=headers))
# Graph the NFA
# TODO : uncomment this to print the NFA
dot = nfa.graphNFA(nfa.result[0])
dot.render('nfa', format='pdf', view=True)
