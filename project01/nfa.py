EMPTY_STRING = ''

def generate_state():
    return State()

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

def union_t_function(t_function1, t_function2):
    t_function = t_function1.copy()
    for key in t_function2.keys():
        if key not in t_function:
            t_function[key] = t_function2[key]
    return t_function

class NFA():
    """Summary of class here.

    Defination of the regular language.

    Attributes:
        alphabet:   list object to store finate alphabet
        states:     list object to store the states
        s_state:    State object (cannot be None)
        f_states:   list object to store the accepted states
        t_function: a nesting dict obejct, whose value is also a dict object
                    that store the states corresponded to the action on the edge
    """
    def __init__(self, alphabet, states, s_state, f_states=[], t_function=None):
        self.alphabet = alphabet
        # use set obejct to define alphabelts
        self.alphabet = set(alphabet)
        self.states = states
        self.s_state = s_state
        self.f_states = f_states
        self.t_function = t_function

        # t_function is None : not given by user
        if t_function is None:
            self.t_function = dict()
            for state in states:
                self.t_function[state] = dict()

    # we will not implement the setter function of states
    # for keeping the orderness of states and protecting
    # states property from being changed by mistakes.
    # same reason for get_states and get_t_function methods
    def get_alphabet(self):
        return self.alphabet

    def get_states(self):
        return self.states

    def get_t_function(self):
        return self.t_function

    def get_f_states(self):
        return self.f_states

    def set_f_states(self, states):
        """set start state
        add a new state, 
        and insert the state in the head of self.states
        Returns:
        Raises:
        """
        self.f_states = states

    def get_start_state(self):
        return self.s_state

    def set_start_state(self, state):
        """set start state
        add a new state, 
        and insert the state in the head of self.states
        Returns:
        Raises:
        """
        self.states.insert(0, state)
        self.s_state = state

#------------------------------------------------------------------------------
# Provide methods for lower-level manipulations of the states object 
#------------------------------------------------------------------------------
    def get_head_state(self):
        assert(len(self.states) > 0)
        return self.states[0]
    
    def get_tail_state(self):
        assert(len(self.states) > 0)
        return self.states[-1]

    def add_state(self, state):
        """add state
        if state in self.states:
            add a new state to self.states
            and add an empty item (which has no aciton) in the self.t_function
        else:
            ignore it
        Returns:
        Raises:
        """
        if state not in self.states:
            self.states.append(state)
            # self.state.insert(0, state)
            self.t_function[state] = dict()

    def add_function_item(self, state, action, to_state):
        """add or change the item in t_function

        first we make sure that every state in states has a dict() value in self.t_function,
        by carefully inserting new state using add_state method and using __init__
        to make sure of it.

        so we only need to check if the state and to_state is in the self.states respectively


        Because NFA have multiple states can be acheived by a single action.
        Then if the action is in the self.t_function[state], we simply append the to_state obejct
        to the self.t_function[state];
        if not, we have to create a list contains the to_state.

        Args:
            state: the key state of the start object
            to_state: a state obeject that is needed to be inserted into
                      the t_function as an item
            action: the action string will be taken for achieving the to_state

        Returns:
        Raises:
            if state or to_state not in the self.states
            then we will raise an assertion error
        """
        assert(state in self.states)
        assert(to_state in self.states)
        if action in self.t_function[state]:
            self.t_function[state][action].append(to_state)
        else:
            self.t_function[state][action] = [to_state]

#------------------------------------------------------------------------------
# Provide methods as the adhesive of nfas
#------------------------------------------------------------------------------
    def or_nfa(self, other_nfa):
        """ provide an or mehotd for oring two nfas

        plz refered to the P68 in the <<Introduction of Theory of Computation>>,
        for it is hard to explain in words.
        QAQ

        Returns: a new nfa contains the result
        Raises:
        """
        new_s_state = generate_state()
        s_state1 = self.get_start_state()
        s_state2 = other_nfa.get_start_state()

        # new_alphabet = self.alphabet + other_nfa.get_alphabet()
        new_alphabet = self.alphabet | other_nfa.get_alphabet() # union operation for set (|)
        # new_states = self.states + other_nfa.get_states()
        new_states = self.states + other_nfa.get_states()# + [new_s_state]
        new_f_states = self.f_states + other_nfa.get_f_states()
        # new_t_fuctions = dict(self.t_function, **other_nfa.t_function)
        new_t_functions = union_t_function(self.t_function, other_nfa.t_function)
        # new_t_functions[new_s_state] = dict()


        # new_t_fuctions[new_s_state][EMPTY_STRING] = [s_state1, s_state2]
        # new_t_functions[new_s_state] = dict()
        # new_t_functions[new_s_state][EMPTY_STRING] = [s_state1, s_state2]

        # nfa = NFA(new_alphabet, new_states, new_s_state, new_f_states, new_t_functions)

        nfa = NFA(new_alphabet, new_states, new_s_state, new_f_states, new_t_functions)
        nfa.add_state(new_s_state)
        nfa.set_start_state(new_s_state)
        nfa.add_function_item(new_s_state, EMPTY_STRING, s_state1)
        nfa.add_function_item(new_s_state, EMPTY_STRING, s_state2)
        return nfa

    def add_nfa(self, other_nfa):
        """ provide an or mehotd for oring two nfas

        plz refered to the P68 in the <<Introduction of Theory of Computation>>,
        for it is hard to explain in words.
        QAQ

        Returns: a new nfa contains the result
        Raises:
        """
        new_alphabet = self.alphabet | other_nfa.get_alphabet() # union operation for set (|)
        new_states = self.states + other_nfa.get_states()
        # new_t_fuctions = dict(self.t_function, **other_nfa.get_t_function())
        # new_t_fuctions = dict(self.t_function.items() + other_nfa.get_t_function().items())
        new_t_fuctions = union_t_function(self.t_function, other_nfa.t_function)

        # nfa = NFA(new_alphabet, new_states, self.s_state, other_nfa.get_f_states(), new_t_fuctions)
        nfa = NFA(new_alphabet, new_states, self.s_state, other_nfa.get_f_states().copy(), new_t_fuctions)

        # we need to add the EMPTY_STRING action to the f_state in self.f_states
        for f_state in self.f_states:
            # we add an item to the self. EMPTY_STRING action, 
            nfa.add_function_item(f_state, EMPTY_STRING, other_nfa.get_start_state())
            # new_t_fuctions[f_state][EMPTY_STRING] = other_nfa.get_start_state()

        return nfa

    def repeat_nfa(self):
        """ provide an or mehotd for oring two nfas

        plz refered to the P68 in the <<Introduction of Theory of Computation>>,
        for it is hard to explain in words.
        QAQ

        Returns: a new nfa contains the result
        Raises:
        """
        # TODO(ShipXu): XiaoHanHou implement this function.
        pass

#------------------------------------------------------------------------------
# Overloaded operators (regard the repeat as an operator)
#------------------------------------------------------------------------------
    def repeat(self):
        return self.repeat_nfa()

    def __add__(self, other):
        return self.add_nfa(other)

    def __or__(self, other):
        return self.or_nfa(other)

    def __str__(self):
        ret = ('------------------NFA desciption------------\n'   +
                'aphabelt : {}'.format(str(self.alphabet))        + '\n' +
                'start state : {}'.format(str(self.s_state))      + '\n' +
                'accepted states : {}'.format(str(self.f_states)) + '\n' +
                'transition fuctions : '                          + '\n')
        for key in self.t_function.keys():
            item_str = str((key, str(self.t_function[key])))
            ret += item_str + '\n'
        return ret

if __name__ == '__main__':
    alphabet = ['a', 'b']

    # test01: generate_state
    s1 = generate_state()
    s2 = generate_state()
    s3 = generate_state()
    print(s1, s2, s3)

    # test02: nfa
    states = [s1, s2]
    s_state = s1
    f_states = [s1, s2]
    nfa = NFA(alphabet, states, s_state, f_states)
    nfa.add_function_item(s1, 'a', s2)
    nfa.add_function_item(s2, 'a', s2)
    print(nfa)

    # generate states variable
    states = []
    for i in range(0, 4):
        states.append(generate_state())
    print(states)

    # test03: nfa a ; nfa b
    nfa1 = NFA(alphabet, states[0:2], states[0], [states[1]])
    nfa1.add_function_item(states[0], 'a', states[1])
    print('-------nfa1--------')
    print(nfa1)
    nfa2 = NFA(alphabet, states[2:4], states[2], [states[3]])
    nfa2.add_function_item(states[2], 'b', states[3])
    print('-------nfa2--------')
    print(nfa2)

    # test04: test for t_function_union
    t_function1 = nfa1.get_t_function()
    t_function2 = nfa2.get_t_function()

    print('-------test_union_function--------')
    print(nfa1.get_t_function())
    print(nfa2.get_t_function())
    print(union_t_function(t_function1, t_function2))

    # test05: test for '+'
    print('-------nfa1 + nfa2--------')
    print(nfa1 + nfa2)

    # test05: test for '|'
    print('-------(nfa1 + nfa2) | nfa1--------')
    print((nfa1 + nfa2) | nfa1)

    # test06: test for '*'(not implemented)
    # print('-------nfa | nfa2--------')
    # print(((nfa1 + nfa2) | nfa1).repeat())