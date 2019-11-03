from regular_expression import RE
from test_REtoNFA import trans_RE_to_NFA, add_parentheses_repeat

if __name__ == '__main__':
    regular_string = '(ab|a)*'
    alphabet = list(set([word for word in regular_string
                    if word.isalpha() or word.isdigit()]))
    re = RE(alphabet, add_parentheses_repeat(regular_string))
    nfa = trans_RE_to_NFA(re)

    with open('test_run_re.txt') as file:
        for line in file.readlines():
            line = line.replace('\n', '')
            if (nfa.run(line)):
                print('matched and matched result {}'.format(line.replace('\n', '')))