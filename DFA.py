from NFA_ import NFA_
from Regex import Regex
from test import *

class DFA:
    def __init__(self, nfa, trans_matrix):
        self.nfa = nfa
        self.e_closures = {state.name:self.epsilon_closure(state.name) for state in self.nfa}
        self.trans_matrix = trans_matrix
        self.result = [['state'] + [header for header in self.trans_matrix[0] if header != 'ε' and header != 'symbols']]
        self.symbols = [symbol for symbol in self.result[0] if symbol != 'state']
        self.stack = []

    def epsilon_closure(self, state_name):
        nfa = self.nfa
        can_move = []
        stack = []
        # Get the initial transition states
        for state in nfa:
            if state.name == state_name:
                try:
                    can_move += state.transitions['ε']
                    stack += state.transitions['ε']
                except:
                    pass
        
        while len(stack) > 0:
            
            for state in nfa:
                if state.name == stack[0]:
                    try:
                        can_move += state.transitions['ε']
                        stack += state.transitions['ε']
                    except:
                        pass
            stack.pop(0)
        
        return can_move

    def symbol_closure(self, state_name, symbol):
        nfa = self.nfa
        can_move = []
        stack = []
        # Get the initial transition states
        for state in nfa:
            if state.name == state_name:
                try:
                    can_move += state.transitions[symbol]
                    stack += state.transitions[symbol]
                except:
                    pass
        
        while len(stack) > 0:
            
            for state in nfa:
                if state.name == stack[0]:
                    try:
                        can_move += state.transitions[symbol]
                        stack += state.transitions[symbol]
                    except:
                        pass
            stack.pop(0)
        
        return can_move

    def showE_closures(self):
        print('epsilon-closures: ')    
        for k,v in self.e_closures.items():
            print(k,v)
    
    def gen_row(self, state):
        new_row = []
        # Getting the first item from the closures dictionary
        first_key = state
        # Appending the first item to the new_row list
        new_row.append(state)
        # For each symbol in the symbols list get the reachable states and append them to the new_row list respectively to the symbol
        for symbol in self.symbols:
            new_state = []
            for state in self.e_closures[first_key]:
                estado = self.symbol_closure(state, symbol)
                if len(estado) != 0:
                    for element in estado:
                        if element in self.e_closures:
                            new_state.append(element)
                            new_state.append(sorted(self.e_closures[element]))
                            
            
            store = []
            for i in new_state:
                if type(i) == str:
                    store.append(i)
                    new_state.remove(i)
            new_state.insert(0,store)
            new_state = [lst for lst in new_state if lst]
            new_row.append(new_state)
            
        return new_row
        
    def merge_states(self, state, state2):
        
        if len(state) == 1 and len(state2) > 1:
            return [self.flatten([state2[0]] + [state]), state2[1:]]

        elif len(state) > 1 and len(state2) == 1:
            return [self.flatten([state[0] + state2]), state[1:]]
        
        elif len(state) == 1 and len(state2) == 1:
            return self.flatten([state[0] + state2[0]])
        
        else:
            result = []
            # Add the first element of both lists
            result.append([state[0], state2[0]])

            # Merge the nested lists and remove duplicates
            for i in range(1, len(state)):
                nested_list = []
                for j in range(len(state[i])):
                    # Check if the inner list is not empty
                    if state[i][j] or state2[i][j]:
                        # Merge the lists and remove duplicates
                        merge_list = state[i][j] + state2[i][j]
                        nested_list.extend([x for x in merge_list if x not in nested_list])
                result.append(nested_list)
        
    def flatten(self,lst):
        flat_list = []
        for item in lst:
            if type(item) == list:
                flat_list.extend(self.flatten(item))
            else:
                flat_list.append(item)
        return flat_list
    
    def gen_from_lastRow(self, result):
        to_iter = result[-1]
        states_to_gen = []
        final = []
        for i in to_iter:
            if type(i) == list:
                states_to_gen.append(i[0])
        for state_s in states_to_gen:
            if len(state_s) > 1:
                resultado = []
                for state in state_s:
                    new_row = self.gen_row(state)
                    new_row = [sublist for sublist in new_row if len(sublist) > 0]
                    resultado.append(new_row)
                
                resultado = self.merge_states(resultado[0], resultado[1])
                final.append(resultado)
            elif len(state_s) == 1:
                new_row = self.gen_row(state_s[0])
                new_row = [sublist for sublist in new_row if len(sublist) > 0]
                final.append(new_row)
        return final
                
    def subconjuntos(self, result):
        while True:
            new_row = dfa.gen_from_lastRow(result)
            if new_row not in dfa.result:
                dfa.result.append(new_row)
                break
    
    def minimizacion(self):
        pass
    #Create a function that applies minimization to the DFA
    
    
# Example of usage
expression = '(a$b|c)*'
postfix = Regex(expression).postfix
print(f'Infix: {expression}\nPostfix: {postfix}')
nfa = NFA_(postfix)
trans_matrix  = nfa.god_func()
dfa = DFA(nfa.result[0], trans_matrix)
dfa.showE_closures()
first_key = next(iter(dfa.e_closures))
row = dfa.gen_row(first_key)
if row not in dfa.result:
    dfa.result.append(row)
dfa = regex_to_dfa(expression)
# Generate a Graphviz graph from the DFA
graph = visualize_dfa(dfa)
graph.render('dfa')

print(dfa)





            

 


            