from visualizer import draw_TM

BLANK = ''
LEFT = 'L'
RIGHT = 'R'
SIGN = '#'

def generate_state():
    return State()

def generate_states(num_states):
    ret_states = []
    for _ in range(0, num_states):
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
        self.name = "q{}".format(State.id)

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
        ret = '(to_state : {} '.format(str(self.to_state))
        if self.t_action is not None:
            ret += 't_action : {} '.format(str(self.t_action))
        ret += 'movement : {})'.format(str(self.movement))
        return ret
    
    def __repr__(self):
        return self.__str__()


class TM():
    """
    Definition of the Turing Machine

    Attributes:
        states:     list object to store the states
        i_alphabet: list object to store input alphabet
        t_alphabet: list object to store tape alphabet
        s_state:    Start state object (cannot be None)
        a_state:    The accept state
        r_state:    The reject state
        t_function: transition function, a nesting dict obejct, whose value is also a dict object.
                    The inner dict stores the corresponded tm_item tuple of action, which contains the new state, t_action that will be
                    written on the tape, and movements
    """
    def __init__(self, states, i_alphabet, t_alphabet, s_state, a_state, r_state, t_function=None):
        self.states = states

        self.i_alphabet = i_alphabet
        self.t_alphabet = t_alphabet

        self.s_state = s_state
        self.a_state = a_state
        self.r_state = r_state

        # t_function is None : not given by user
        if t_function is None:
            self.t_function = dict()
            for state in states:
                self.t_function[state] = dict()

    def get_i_alphabet(self):
        return self.i_alphabet

    def get_t_alphabet(self):
        return self.t_alphabet

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

        # if action in self.t_function[state]:
        #     if tm_item not in self.t_function[state][action]:
        #         self.t_function[state][action].append(tm_item)
        # else:
            # self.t_function[state][action] = [tm_item]
        self.t_function[state][action] = tm_item


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

    def _run(self, tape, present_node, tape_index=0):
        if present_node is self.get_a_state():
            return True

        if present_node is self.get_r_state():
            return False

        assert(tape_index >= 0 and tape_index < len(tape))
        head_w = tape[tape_index]

        if head_w in self.t_function[present_node]:
            tm_item = self.t_function[present_node][head_w]

            if tm_item.t_action != None:
                tape[tape_index] = tm_item.t_action

            tape_index = move_tape_head(tape_index, tm_item.movement)
            to_node = tm_item.to_state
            return self._run(tape, to_node, tape_index)

        return False

    def run(self, tape):
        return self._run(tape, self.s_state)

def move_tape_head(tape_index, movement):
        if movement == LEFT:
            if tape_index <= 0:
                # if TM ever tries to move its head to the leaft off the left-hand end of the tape
                # the head stays in the same place for that move, even though the transition function
                # indicates L
                return 0
            return tape_index - 1
        if movement == RIGHT:
            return tape_index + 1

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

    i_alphabet = ['0']
    t_alphabet = ['0', 'x', BLANK]

    tm = TM(states, i_alphabet, t_alphabet, s_state, a_state, r_state)

    tm.add_tm_item(states[0], BLANK, r_state, None, RIGHT)
    tm.add_tm_item(states[0], 'x', r_state, None, RIGHT)
    tm.add_tm_item(states[0], '0', states[1], BLANK, RIGHT)

    tm.add_tm_item(states[1], BLANK, a_state, None, RIGHT)
    tm.add_tm_item(states[1], 'x', states[1], None, RIGHT)
    tm.add_tm_item(states[1], '0', states[2], 'x', RIGHT)

    tm.add_tm_item(states[2], '0', states[3], None, RIGHT)
    tm.add_tm_item(states[2], 'x', states[2], None, RIGHT)
    tm.add_tm_item(states[2], BLANK, states[4], None, LEFT)

    tm.add_tm_item(states[3], BLANK, r_state, None, RIGHT)
    tm.add_tm_item(states[3], 'x', states[3], None, RIGHT)
    tm.add_tm_item(states[3], '0', states[2], 'x', RIGHT)

    tm.add_tm_item(states[4], '0', states[4], None, LEFT)
    tm.add_tm_item(states[4], 'x', states[4], None, LEFT)
    tm.add_tm_item(states[4], BLANK, states[1], None, RIGHT)

    print(tm)

    tape = list('0000')
    tape.append(BLANK)
    print(tape)
    print(tm.run(tape))

    # draw_TM(tm)