from State import NFAState
from tabulate import tabulate
from Regex import Regex
from graphviz import Digraph


class NFA_:
    def __init__(self, postfix):
        self.start_state = None
        self.final_state = None
        self.state_count = 0
        self.result = self.Thompson(postfix)
        self.transmatrix = self.gen_trans_matrix()
        
    def create_nfa_for_character(self, char):
        start_state = NFAState()
        end_state = NFAState()
        start_state.addName(f'q{self.state_count}')
        self.state_count += 1
        end_state.addName(f'q{self.state_count}')
        self.state_count += 1
        
        if char == '$':
            # Add epsilon transition from the start state to the end state
            start_state.transitions['ε'] = [end_state.name]
        else:
            # Add transition for the current character
            start_state.transitions[char] = [end_state.name]

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
        # If nfa2 is empty, return nfa1 unchanged
        if len(nfa2) == 0:
            return nfa1

        # Merge the final state of the first NFA with the start state of the second NFA
        nfa1[-1].transitions = nfa2[0].transitions
        nfa2.pop(0)
        nfa1.append(nfa2.pop())

        # Rearrange the names of states
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
        # Initialize empty stack
        stack = []

        # Traverse postfix expression
        for char in postfix_expression:

            if char == '|':
                # Pop two NFAs from stack, take union, and push result onto stack
                nfa2 = stack.pop()
                nfa1 = stack.pop()
                nfa = self.union(nfa1, nfa2)
                stack.append(nfa)
                self.state_count = len(stack[0])

            elif char == '*':
                # Pop single NFA from stack, apply Kleene star to it, and push result back onto stack
                nfa = stack.pop()
                nfa = self.kleene_star(nfa)
                stack.append(nfa)
                self.state_count = len(stack[0])

            elif char == '$':
                # Pop two NFAs from stack, concatenate them, and push result onto stack
                nfa2 = stack.pop()
                nfa1 = stack.pop()
                nfa = self.concatenate(nfa1, nfa2)
                stack.append(nfa)
                self.state_count = len(stack[0])

            elif char.isalpha() or char.isnumeric():
                # Create an NFA for the character
                nfa = self.create_nfa_for_character(char)
                stack.append(nfa)

        # Set the initial and final states of the resulting NFA
        self.initial_state = stack[0][0].name
        self.final_state = stack[0][-1].name

        # Return the NFA
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
    
    def visualize_nfa(self):
        nfa = self.result[0]
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


    def god_func(self):
        print(f'Initial State: {self.initial_state}\nFinal State: {self.final_state}\n\nNFA: ')
        print(f'\n{self.showNFA(self.result[0])}\n')
        graph = self.visualize_nfa()
        graph.render('nfa.pdf', view=False)
        return self.gen_trans_matrix()


# Example of usage
expression = '(a|b)*'
postfix = Regex(expression).postfix
print(f'Infix: {expression}\nPostfix: {postfix}')
nfa = NFA_(postfix)
trans_matrix  = nfa.god_func()

print(trans_matrix)
