
from regular_expression import RE
from nfa import NFA, State
from nfa import generate_state

EMPTY_STRING = ''

def generate_head_nfa():
    s0 = generate_state()
    nfa = NFA(re.alphabet, [s0], s0, [])
    return nfa

def generate_aciton_nfa(action):
    nfa = generate_head_nfa()
    f_state = generate_state()
    nfa.add_state(f_state)
    nfa.add_function_item(nfa.get_start_state(),
                          action,
                          f_state)
    return nfa

def read_add(s, nfa1):
    # s_state1 = nfa1.get_start_state()
    nfa2 = _trans_RE_to_NFA(s)
    # s_state2 = nfa2.get_start_state()
    return nfa1 + nfa2

def read_or(s, nfa1):
    nfa2 = _trans_RE_to_NFA(s)
    return nfa1 | nfa2

def read_repeat(s, nfa):
    return read_token(s, nfa.repeat())

def read_parentheses(s, nfa):
    pass

def read_add(action, nfa):
    # new_state = generate_state()
    # new_nfa = generate_head_nfa()
    # new_nfa.add_state(new_state)
    action_nfa = generate_aciton_nfa(action)

    # get the tail node of nfa(named as pre_tail_node), and add a new state to the nfa
    # nfa.add_state(new_state)
    # for pre_tail_state in nfa.get_f_states():
    #     nfa.add_function_item(pre_tail_state, action, new_state)

    # use the tail state in the normal nfa to be final states
    # nfa.set_f_states([new_state])
    return nfa + action_nfa

def read_token(s, nfa):
    # s is empty or s is None
    if not s:
        return nfa

    if s[0] == '*':
        return read_or(s[1:], nfa)
    elif s[0] == '|':
        return read_repeat(s[1:], nfa)
    elif s[0] == '(':
        return read_parentheses(s[1:], nfa)
    else:
        return read_token(s[1:], read_add(s[0], nfa))

def _trans_RE_to_NFA(s):
    nfa = generate_head_nfa()
    return read_token(s, nfa)

def trans_RE_to_NFA(re):
    return _trans_RE_to_NFA(re.s)

if __name__ == '__main__':
    alphabelts = ['0', '1']
    re = RE(alphabelts, '01') #.add_rl(RE(alphabelts, '10')
    nfa = trans_RE_to_NFA(re)
    print(nfa)