EMPTY_STRING = ''

class RE():
    """Defination of the regular language.

    Attributes:
<<<<<<< Updated upstream
        s: the string to describe the regular language 

=======
        s: the string that describes the regular language
        alphabet: list object to store finite alphabet
>>>>>>> Stashed changes
    """
    def __init__(self, alphabet, s):
        # TODO check is word in s is in the alphabet
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
# when alphabet is given
EMPTY_RE = (lambda alphabet: RE(alphabet, EMPTY_STRING))

def get_alphabelt_re(alphabet):
    ret = EMPTY_RE(alphabet)

    if alphabet:
        ret = RE(alphabet, alphabet[0])
        for a in alphabet[1:]:
            ret |= RE(alphabet, a)
    return ret()

if __name__ == '__main__':
    alphabet = ['0', '1']

    re_01 = (lambda s: RE(alphabet, s))
    print(re_01('0').repeat())

    # test practices in P65 of book
    # test01: 0*10*
    # print(RE(alphabet, '0'))
    print(re_01('0').repeat() + re_01('1') + re_01('0').repeat())

    # test02: (alphabet)*1(alphabet)*
    re_alphabet = get_alphabelt_re(alphabet)
    print(re_alphabet.repeat() + re_01('1') + re_alphabet.repeat())

    # test03: 01 | 10
    print(re_01('01') | re_01('10'))