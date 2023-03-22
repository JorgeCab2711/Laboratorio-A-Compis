from State import NFAState
from tabulate import tabulate
from Regex import Regex

from tabulate import tabulate

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
        print('Union')
        new_nfa = []
        
        neg_index = int(nfa1[0].name.replace('q', ''))-1
        neg_state_name =  f'q{neg_index}'
        
        
        # Create a new start state and a new final state
        new_start_state = NFAState(neg_state_name)
        new_final_state = NFAState(f'q{self.state_count}')
        
        self.state_count += 2
        
        # Add epsilon transitions from the new start state to the start states of the two NFAs
        new_start_state.add_transition('ε', [nfa1[0].name, nfa2[0].name])
        
        
        
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
        
        print('Kleene star')
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


    

expression = '(a$b$c$d$f)*'
postfix = Regex(expression).postfix
print(f'Infix: {expression}\nPostfix: {postfix}')
nfa = NFA(postfix)
print('Initial state:', nfa.initial_state)
print('Final state:', nfa.final_state)
print('NFA Transition table:')
nfa.showNFA(nfa.result)
print(nfa.state_count)

    