from graphviz import Digraph

BLANK = ''
LEFT = 'L'
RIGHT = 'R'

def generate_state():
    return State()

def generate_states(num_states):
    ret_states = []
    for i in range(0, num_states):
        ret_states.append(generate_state())
    return ret_states

def union_t_function(t_function1, t_function2):
    t_function = {}
    for key in t_function1.keys():
        t_function[key] = t_function1[key].copy()

    for key in t_function2.keys():
        if key not in t_function:
            t_function[key] = t_function2[key].copy()
        else:
            t_function[key] += t_function2[key].copy()
    return t_function


class State():
    id = 0

    def __init__(self):
        # use static id to identify the nodes
        State.id += 1
        self.name = "node{}".format(State.id)

    def getName(self):
        return self.name

    def __str__(self):
        return self.getName()

    def __repr__(self):
        # repr : used when transforming ab object to string
        return str(self)


class TM_Item():
    def __init__(self, to_state, t_action, movement):
        self.to_state = to_state
        self.t_action = t_action
        self.movement = movement
    
    def __str__(self):
        ret = 'to_state : {} '.format(str(self.to_state))
        if self.t_action is not None:
            ret += 't_action : {} '.format(str(self.t_action))
        ret += 'movement : {}'.format(str(self.movement))
        return ret
    
    def __repr__(self):
        return self.__str__()


class TM():
    """
    Definition of the Nondeterministic Finite Automaton.

    Attributes:
        alphabet:   list object to store finate alphabet
        states:     list object to store the states
        s_state:    State object (cannot be None)
        f_states:   list object to store the accepted states
        t_function: a nesting dict obejct, whose value is also a dict object
                    that store the states corresponded to the action on the edge
    """
    def __init__(self, states, s_state, a_state, r_state, t_function=None):
        self.states = states

        # use set obejct to define alphabelts
        # self.i_alphabet = set(i_alphabet)
        # self.t_alphabet = set(t_alphabet)

        self.s_state = s_state
        self.a_state = a_state
        self.r_state = r_state

        # t_function is None : not given by user
        if t_function is None:
            self.t_function = dict()
            for state in states:
                self.t_function[state] = dict()

    # def get_i_alphabet(self):
    #     return self.i_alphabet

    # def get_t_alphabet(self):
    #     return self.t_alphabet

    def get_s_state(self):
        return self.s_state

    def get_a_state(self):
        return self.a_state

    def get_r_state(self):
        return self.r_state

    def get_t_function(self):
        return self.t_function

    def _add_tm_item(self, state, action, tm_item):
        to_state = tm_item.to_state
        assert(state in self.states)
        assert(to_state in self.states)

        if action in self.t_function[state]:
            if tm_item not in self.t_function[state][action]:
                self.t_function[state][action].append(tm_item)
        else:
            self.t_function[state][action] = [tm_item]

    def add_tm_item(self, state, action, to_state, t_action, movement):
        tm_item = TM_Item(to_state, t_action, movement)
        to_state = tm_item.to_state
        assert(state in self.states)
        assert(to_state in self.states)
        self._add_tm_item(state, action, tm_item)

#------------------------------------------------------------------------------
# Overloaded operators
#------------------------------------------------------------------------------
    def __str__(self):
        ret = ('------------------NFA desciption------------\n'   +
                'states : {}'.format(str(self.states))            + '\n' +
                'start state : {}'.format(str(self.s_state))      + '\n' +
                'accept state : {}'.format(str(self.a_state))     + '\n' +
                'reject state : {}'.format(str(self.r_state))     + '\n' +
                'transition fuctions : '                          + '\n')
        for key in self.t_function.keys():
            item_str = str((key, str(self.t_function[key])))
            ret += item_str + '\n'
        return ret

    def run(self, s, present_node):
        # tape_index = 0

        # if present_node is self.get_s_state():
        #     return True

        # if present_node is self.get_r_state():
        #     return False
        pass

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
    graph.node('%s'%s_node, shape="doublecircle")

    a_node = tm.get_a_state()
    graph.node('%s'%a_node, shape="doublecircle")
    r_node = tm.get_r_state()
    graph.node('%s'%r_node, shape="doublecircle")

    for node in tm.t_function.keys(): 
        if node != s_node and node != a_node and node != r_node:
            graph.node('%s'%node, shape="circle")

        for action in tm.t_function[node].keys():
            for tm_item in tm.t_function[node][action]:
                to_node = tm_item.to_state
                if action == BLANK:
                    graph.edge('%s'%node, '%s'%to_node,
                               '%s'%('{} -> {}'.format('_', get_print_item(tm_item))))
                else:
                    graph.edge('%s'%node, '%s'%to_node,
                               '%s'%('{} -> {}'.format(action, get_print_item(tm_item))))
    
    _s_node = ''
    graph.node(_s_node, shape="circle", color='white')
    graph.edge(_s_node, '%s'%s_node)
    graph.view()

if __name__ == '__main__':
    states = []

    for i in range(0, 7):
        states.append(generate_state())
    print(states)

    inputs = []
    tape = []

    s_state = states[0]
    a_state = states[5]
    r_state = states[6]

    tm = TM(states, s_state, a_state, r_state)

    tm.add_tm_item(states[0], BLANK, r_state, None, RIGHT)
    tm.add_tm_item(states[0], 'x', r_state, None, RIGHT)
    tm.add_tm_item(states[0], '0', states[1], BLANK, RIGHT)

    tm.add_tm_item(states[1], BLANK, a_state, None, RIGHT)
    tm.add_tm_item(states[1], 'x', states[1], None, RIGHT)
    tm.add_tm_item(states[1], '0', states[2], 'x', RIGHT)

    tm.add_tm_item(states[2], '0', states[3], None, RIGHT)
    tm.add_tm_item(states[2], '0', states[2], None, RIGHT)
    tm.add_tm_item(states[2], BLANK, states[4], None, LEFT)

    tm.add_tm_item(states[3], BLANK, r_state, None, RIGHT)
    tm.add_tm_item(states[3], 'x', states[3], None, RIGHT)
    tm.add_tm_item(states[3], '0', states[2], 'x', RIGHT)

    tm.add_tm_item(states[4], '0', states[4], None, LEFT)
    tm.add_tm_item(states[4], 'x', states[4], None, LEFT)
    tm.add_tm_item(states[4], BLANK, states[1], None, RIGHT)

    print(tm)
    draw_TM(tm)