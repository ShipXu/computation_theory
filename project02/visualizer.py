from graphviz import Digraph
BLANK = ''

def get_print_item(tm_item):
    ret = ''

    if tm_item.t_action != None:
        if tm_item.t_action != BLANK:
            ret += '{},'.format(str(tm_item.t_action))
        else:
            ret += '_,'

    ret += str(tm_item.movement)
    return ret

def draw_TM(tm):
    graph = Digraph()

    s_node = tm.get_s_state()
    graph.node('%s'%s_node, shape="circle")

    a_node = tm.get_a_state()
    graph.node('q_accept', shape="circle")
    r_node = tm.get_r_state()
    # graph.node('q_reject', shape="circle")

    for node in tm.t_function.keys(): 
        if node != s_node and node != a_node and node != r_node:
            graph.node('%s'%node, shape="circle")

        t_dict = {}
        for action in tm.t_function[node].keys():
            tm_item = tm.t_function[node][action]
            to_node = tm_item.to_state
            if action == BLANK:
                t_string = '{} -> {}'.format('_', get_print_item(tm_item))
            else:
                t_string = '{} -> {}'.format(action, get_print_item(tm_item))

            if to_node not in t_dict:
                t_dict[to_node] = t_string
            else:
                t_dict[to_node] +=  '\n' + t_string

        for to_node in t_dict.keys():
            if to_node == a_node:
                graph.edge('%s'%node, 'q_accept', t_dict[to_node])
            elif to_node == r_node:
                graph.edge('%s'%node, 'q_reject', t_dict[to_node])
            else:
                graph.edge('%s'%node, '%s'%to_node, t_dict[to_node])

    _s_node = ''
    graph.node(_s_node, shape="circle", color='white')
    graph.edge(_s_node, '%s'%s_node)
    # graph.graph_attr['rankdir'] = 'LR'
    graph.view()
