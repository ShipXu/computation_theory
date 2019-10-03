EMPTY_STRING = ''

class RE():
    """Defination of the regular language.

    Attributes:
        s: the string to describe the regular language 

    """
    def __init__(self, alphabet, s):
        # TODO check is word in s is in the alphabeta
        self.alphabet = alphabet
        self.s = s

    def add_re(self, other_re):
        # return RE(self.alphabet, self.s + '+' + other_re.s)
        return RE(self.alphabet, self.s + other_re.s)

    def repeat(self):
        return RE(self.alphabet, self.s + '*')

    def or_re(self, other_re):
        return RE(self.alphabet, self.s + '|' + other_re.s)

    def call_re(self):
        return RE(self.alphabet, '(' + self.s + ')')

    def __or__(self, other):
        return self.or_re(other)

    def __add__(self, other):
        return self.add_re(other)

    def __call__(self):
        # deal with the X() situation
        return self.call_re()

    def __str__(self):
        # deal with the print(situation)
        return self.s

# a function object that can used to produce a re object
# when alphabelt is given 
EMPTY_RE = (lambda alphabelt: RE(alphabelt, EMPTY_STRING))

def get_alphabelt_re(alphabelt):
    ret = EMPTY_RE(alphabelt)

    if alphabelt:
        ret = RE(alphabelt, alphabelt[0])
        for a in alphabelt[1:]:
            ret |= RE(alphabelt, a)
    return ret()

if __name__ == '__main__':
    alphabelt = ['0', '1']

    re_01 = (lambda s: RE(alphabelt, s))
    print(re_01('0').repeat())

    # test pratices in P65 of book
    # test01: 0*10*
    # print(RE(alphabelt, '0'))
    print(re_01('0').repeat() + re_01('1') + re_01('0').repeat())

    # test02: (alphabelt)*1(alphabelt)*
    re_alphabeta = get_alphabelt_re(alphabelt)
    print(re_alphabeta.repeat() + re_01('1') + re_alphabeta.repeat())

    # test03: 01 | 10
    print(re_01('01') | re_01('10'))