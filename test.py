import re
import graphviz
from automata.fa.nfa import NFA
from automata.fa.dfa import DFA

def regex_to_dfa(regex:str):
    regex =  regex.replace('$', '')
    # Compile the regular expression into a pattern
    pattern = re.compile(regex)

    # Extract the underlying NFA (Nondeterministic Finite Automaton) from the pattern
    nfa = NFA.from_regex(regex)

    # Convert the NFA to a DFA (Deterministic Finite Automaton) using the subset construction algorithm
    dfa = DFA.from_nfa(nfa)

    return dfa


def visualize_dfa(dfa):
    # Create a new Graphviz Digraph object
    graph = graphviz.Digraph()

    # Add the nodes to the graph
    for state in dfa.states:
        if state in dfa.final_states:
            # Add a double-circle node for final states
            graph.node(str(state), shape='doublecircle')
        else:
            # Add a circle node for non-final states
            graph.node(str(state), shape='circle')

    # Add the edges to the graph
    for start_state, transitions in dfa.transitions.items():
        for symbol, end_state in transitions.items():
            graph.edge(str(start_state), str(end_state), label=symbol)

    return graph




