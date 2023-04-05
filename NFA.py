from State import NFAState
from tabulate import tabulate
from Regex import Regex
from graphviz import Digraph


class NFA:
    def __init__(self, postfix):
        self.start_state = None
        self.final_state = None
        self.state_count = 0
        self.result = self.Thompson(postfix)
        
        
    def create_nfa_for_character(self, char):
        start_state = NFAState()
        end_state = NFAState()
        start_state.addName(f'q{self.state_count}')
        self.state_count += 1
        end_state.addName(f'q{self.state_count}')
        start_state.transitions[char] = [end_state.name]
        self.state_count += 1
        return [start_state, end_state]
    
    def showNFA(self, nfa):
        try:
            type(nfa[0][0]) == NFAState
            for i in nfa:
                for state in i:
                    print(state.name,'-->', state.transitions)
                    
        except:
            for i in nfa:
                if i is not None:
                    print(i.name,'-->', i.transitions)
                
        
    def concatenate(self, nfa1, nfa2):
        # Merge the final state of the first NFA with the start state of the second NFA
        if len(nfa2) == 0:
            # If nfa2 is empty, return nfa1 unchanged
            return nfa1
        else:
            nfa1[-1].transitions = nfa2[0].transitions
            nfa2.pop(0)
            nfa1.append(nfa2.pop())
        
        # Rearrage te names of states
        for i in range(len(nfa1)):
            for symbol in nfa1[i].transitions:
                nfa1[i].name = f'q{i}'
                nfa1[i].transitions[symbol] = [f'q{i+1}']
        
        nfa1[-1].name = f'q{len(nfa1)-1}'
        

        return nfa1

     
    def union(self, nfa1, nfa2):
        new_nfa = []
        
        neg_index = int(nfa1[0].name.replace('q', ''))-1
        neg_state_name =  f'q{neg_index}'
        
        
        # Create a new start state and a new final state
        new_start_state = NFAState(neg_state_name)
        new_final_state = NFAState(f'q{self.state_count}')
        
        self.state_count += 2
        
        # Add epsilon transitions from the new start state to the start states of the two NFAs
        new_start_state.add_transition('ε')
        new_start_state.transitions['ε'] = [nfa1[0].name, nfa2[0].name] 
        
        
        
        # Add epsilon transitions from the final states of the two NFAs to the new final state
        nfa1[-1].add_transition('ε', new_final_state.name)
        nfa2[-1].add_transition('ε', new_final_state.name)
        # Inserting the new start state to the beginning of the nfa1
        new_nfa.append(new_start_state)
        
        for i in nfa1:
            new_nfa.append(i)
        for i in nfa2:
            new_nfa.append(i)
        
        new_nfa.append(new_final_state)
        
        return new_nfa
        
    def kleene_star(self, nfa):
        new_nfa = []
        
        neg_index = int(nfa[0].name.replace('q', ''))-1
        neg_state_name =  f'q{neg_index}'
        
        
        # Create a new start state and a new final state
        new_start_state = NFAState(neg_state_name)
        new_final_state = NFAState(f'q{self.state_count}')
        
        self.state_count += 2
        
        
        new_start_state.add_transition('ε', nfa[0].name)
        new_start_state.add_transition('ε', new_final_state.name)
        nfa[-1].add_transition('ε', nfa[0].name)
        nfa[-1].add_transition('ε', new_final_state.name)
        
        
        new_nfa.append(new_start_state)
        
        for i in nfa:
            new_nfa.append(i)
        
        new_nfa.append(new_final_state)
        
        
        return new_nfa  
        
    def Thompson(self, postfix_expression):
        stack = []
        for char in postfix_expression:
            if char in ['|','+']:
                # Union operation
                nfa2 = stack.pop()
                nfa1 = stack.pop()
                nfa = self.union(nfa1, nfa2)
                stack.append(nfa)
                self.state_count = len(stack[0])
                
            elif char == '$':
                # Concatenation operation
                nfa2 = stack.pop()
                nfa1 = stack.pop()
                nfa = self.concatenate(nfa1, nfa2)
                stack.append(nfa)
                self.state_count = len(stack[0])
                
            elif char == '*':
                # Kleene star operation
                nfa1 = stack.pop()
                nfa = self.kleene_star(nfa1)
                stack.append(nfa)
                self.state_count = len(stack[0])
                pass
            elif char == '?':
                # Optional operation
                pass
            elif char.isalpha() or char.isnumeric():
                # Create an NFA for the character
                nfa = self.create_nfa_for_character(char)
                
                stack.append(nfa)
            
        self.initial_state = stack[0][0].name
        self.final_state = stack[0][-1].name
        # Return the final NFA
        
        return stack

    def gen_trans_matrix(self):
        symbols = []
        states = []
        trans_matrix = {}
        for state in self.result[0]:
            for symbol in state.transitions:
                if symbol not in symbols:
                    symbols.append(symbol)
            if state.name not in states:
                states.append(state.name)
        
        # Create an empty transition matrix with headers
        trans_matrix = {}
        trans_matrix['symbols'] = symbols.copy() # copy symbols to avoid aliasing
        for state in states:
            trans_matrix[state] = ['']*len(symbols)

        # Populate transition matrix with state transitions for each symbol
        for state in self.result[0]:
            for symbol in state.transitions:
                # Get the index of the symbol in the matrix
                symbol_idx = symbols.index(symbol)
                # Get the name of the state that the transition leads to
                next_state_name = state.transitions[symbol]
                # Add the next state name to the matrix at the corresponding position
                trans_matrix[state.name][symbol_idx] = next_state_name
                
        
        # Convert transition matrix to list of lists
        trans_matrix = [trans_matrix['symbols']] + [[k] + v for k, v in trans_matrix.items() if k != 'state']
        trans_matrix = trans_matrix[1:]
        return trans_matrix
    

def visualize_nfa(nfa):
    # Create a new graph
    graph = Digraph()
    
    graph.attr(rankdir='LR')
    
    # Set the default node attributes
    graph.node_attr.update(shape='circle')
    
    # Add the nodes to the graph
    for i, state in enumerate(nfa):
        # If this is the final state, add a double circle around it
        if i == len(nfa) - 1:
            graph.node(state.name, shape='doublecircle')
        else:
            graph.node(state.name)
            
        # Add the transitions from this state to other states
        for symbol, targets in state.transitions.items():
            for target in targets:
                # Use ε to represent an epsilon transition
                label = 'ε' if symbol is None else symbol
                
                graph.edge(state.name, target, label=label)
    
    # Return the Graphviz object
    return graph


# Example of usage
expression = '(a$b)*$c'
postfix = Regex(expression).postfix
print(f'Infix: {expression}\nPostfix: {postfix}')
nfa = NFA(postfix)
print('Initial state:', nfa.initial_state)
print('Final state:', nfa.final_state)
graph = visualize_nfa(nfa.result[0])
graph.render('nfa.pdf', view=False)
nfa.showNFA(nfa.result[0])

# # Transition matrix of the NFA where the first element of the list is the header (symbols)
# trans_matrix  = nfa.gen_trans_matrix()

# # Print transition matrix with tabulate
# print(tabulate(trans_matrix, headers='firstrow'))

# print(trans_matrix[1])
# Example
# for state in nfa.result[0]:
#     for transition in state.transitions:
#         if transition == key:
#             print(state.name,'has a ','transition',state.transitions[transition], 'has key', key)

# closures = {}
# for state in nfa.result[0]:
#     for transition in state.transitions:
#         if transition == 'ε':
#             closures[state.name] = state.transitions[transition]
            
# print(closures)

