from NFA import *
from Regex import Regex

class DFA:
    def __init__(self, nfa):
        self.nfa = nfa
        self.e_closures = {state.name:self.epsilon_closure(state.name) for state in self.nfa}
        self.afd = []
        self.symbols = []


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
    
    def gen_row(self,state):
        new_row = []
        # Getting the first item from the closures dictionary
        first_key = state
        
        # Appending the first item to the final_new_state list
        new_row.append(state)
        # For each symbol in the symbols list get the reachable states and append them to the final_new_state list respectively to the symbol
        for symbol in self.symbols:
            new_state = []
            for state in self.e_closures[first_key]:
                estado = self.symbol_closure(state, symbol)
                
                if len(estado) != 0:
                    for element in estado:
                        if element in self.e_closures:
                            new_state.append(element)
                            new_state.append(self.e_closures[element])
            new_row.append(sorted(self.flatten(new_state)))
        
        if new_row not in self.afd:    
            self.afd.append(new_row)
        
        return new_row
    
    def gen_row_results(self,state):
        new_row = []
        # Getting the first item from the closures dictionary
        first_key = state
        # For each symbol in the symbols list get the reachable states and append them to the final_new_state list respectively to the symbol
        for symbol in self.symbols:
            new_state = []
            for state in self.e_closures[first_key]:
                estado = self.symbol_closure(state, symbol)
                
                if len(estado) != 0:
                    for element in estado:
                        if element in self.e_closures:
                            new_state.append(element)
                            new_state.append(self.e_closures[element])
            new_row.append(sorted(self.flatten(new_state)))
        
        
        return new_row
    
    
    def build_first_row(self, trans_matrix):
        
        self.afd = [['state'] + [header for header in trans_matrix[0] if header != 'ε' and header != 'symbols']] 
        self.symbols = [symbol for symbol in self.afd[0] if symbol != 'state']

        
        # Getting the first item from the closures dictionary
        first_key = next(iter(self.e_closures))
        self.gen_row(first_key)
        
        # si los estados generados no estan en la primera columna del afd agregarlos
        
        for row in self.afd:
            for element in row:
                if type(element) != str and element not in [row[0] for row in self.afd]:
                    element = [element]
                    for i in element[0]:
                        print(i)
                        add = self.gen_row_results(i)
                        if self.flatten(add) != []:
                            print(add)
                        
                        
                    # self.afd.append(element)
                
            
        
        
        
                
        print('raw:')
        print(self.afd)
        print('fixed')
        for i in self.afd:
            print(i)
        
        return self.afd
    
    def flatten(self,lst):
        flat_list = []
        for item in lst:
            if type(item) == list:
                flat_list.extend(self.flatten(item))
            else:
                flat_list.append(item)
        return flat_list


    
# Example of usage
expression = '(a$a|b)*'
postfix = Regex(expression).postfix
print(f'Infix: {expression}\nPostfix: {postfix}')
nfa = NFA(postfix)
afn_matrix  = nfa.god_func()

print('\nNFA to DFA\n')
last_nfa = nfa.result[0] 

dfa = DFA(last_nfa)
head_N_firstR = dfa.build_first_row(afn_matrix)


