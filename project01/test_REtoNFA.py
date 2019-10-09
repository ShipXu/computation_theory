
from regular_expression import RE
from nfa import NFA, State
from nfa import generate_state

EMPTY_STRING = ''

def generate_head_nfa(alphabet):
    s0 = generate_state()
    nfa = NFA(alphabet, [s0], s0, [])
    return nfa

def generate_aciton_nfa(action, alphabet):
    nfa = generate_head_nfa(alphabet)
    f_state = generate_state()
    nfa.add_f_state(f_state)
    nfa.add_function_item(nfa.get_start_state(),
                          action,
                          f_state)
    return nfa

def read_or(s, alphabet, nfa1):
    nfa2 = _trans_RE_to_NFA(s, alphabet)
    return nfa1 | nfa2

def read_repeat(s, alphabet, nfa):
    assert(nfa is not None)
    return read_token(s, alphabet, nfa.repeat())

def read_parentheses(s, nfa):
    # Your code here
    if s[0].current() == ")":
        s.pop()
        return nfa
    return 
    pass

def read_add(action, alphabet, nfa=None):
    action_nfa = generate_aciton_nfa(action, alphabet)
    if nfa is None:
        return action_nfa
    else:
        return nfa + action_nfa

def read_token(s, alphabet, nfa=None):
    # s is empty or s is None
    if not s:
        return nfa

    if s[0] == '*':
        return read_repeat(s[1:], alphabet, nfa)
    elif s[0] == '|':
        return read_or(s[1:], alphabet, nfa)
    elif s[0] == '(':
        return read_parentheses(s[1:], nfa)
    else:
        return read_token(s[1:], alphabet, read_add(s[0], alphabet, nfa))

def _trans_RE_to_NFA(s, alphabet):
    return read_token(s, alphabet)

def trans_RE_to_NFA(re):
    return _trans_RE_to_NFA(re.s, re.alphabet)

if __name__ == '__main__':
    alphabet = ['a', 'b']


    # test01 nfa1
    # action = 'a'
    # nfa = generate_aciton_nfa(action, alphabet)
    # print(nfa)
    # nfa1 = read_add('b', alphabet, nfa)
    # print(nfa1)

    # re = RE(alphabet, 'ab|a')
    re = RE(alphabet, 'a*')
    nfa = trans_RE_to_NFA(re)
    print(nfa)