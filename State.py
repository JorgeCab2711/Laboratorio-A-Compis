class NFAState:
    def __init__(self, name =None, transitions= None):
        self.name = name
        self.transitions = transitions if transitions is not None else {}
        
    def add_transition(self, symbol, states=None):
        if symbol not in self.transitions:
            self.transitions[symbol] = []
        self.transitions[symbol].append(states)

    def addName(self, name):
        self.name = name