from nfa import EMPTY_STRING
from regular_expression import RE
from test_REtoNFA import trans_RE_to_NFA, add_parentheses_repeat
from graphviz import Digraph

if __name__ == '__main__':
    regular_string = 'aa*|ab(ab)*'
    alphabet = list(set([word for word in regular_string
                    if word.isalpha() or word.isdigit()]))
    re = RE(alphabet, add_parentheses_repeat(regular_string))
    nfa = trans_RE_to_NFA(re)
    print(nfa)

    graph = Digraph()
    s_node = nfa.get_start_state()
    _s_node = ''
    graph.node(_s_node, shape="circle", color='white')

    for f_node in nfa.get_f_states():
        graph.node('%s'%f_node, shape="doublecircle")

    for node in nfa.t_function.keys(): 
        # if node == nfa.s_state or node in nfa.f_states:
        if node not in nfa.get_f_states():
            graph.node('%s'%node, shape="circle")
        for action in nfa.t_function[node].keys():
            for to_node in nfa.t_function[node][action]:
                if action == EMPTY_STRING:
                    graph.edge('%s'%node, '%s'%to_node, 'ε')
                else:
                    graph.edge('%s'%node, '%s'%to_node, '%s'%action)

    graph.edge(_s_node, '%s'%s_node)
    graph.graph_attr['rankdir'] = 'LR'
    graph.view()
    # graph.format = 'png'
    # graph.render('output-graph.gv', view=True)