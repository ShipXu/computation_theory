from turing_machine import TM
from turing_machine import generate_states
from visualizer import draw_TM
from turing_machine import BLANK, SIGN, LEFT, RIGHT

if __name__ == '__main__':
    states = generate_states(17)

    inputs = []
    tape = []

    s_state = states[0]
    a_state = states[16]

    i_alphabet = ['a', 'b', 'c', 'd']
    t_alphabet = ['a', 'b', 'c', 'd', BLANK, SIGN]

    tm = TM(states, i_alphabet, t_alphabet, s_state, a_state, None)

    tm.add_tm_item(states[0], SIGN, states[1], None, RIGHT)

    tm.add_tm_item(states[1], 'a', states[2], None, RIGHT)

    tm.add_tm_item(states[2], 'a', states[2], None, RIGHT)
    tm.add_tm_item(states[2], 'b', states[3], None, RIGHT)

    tm.add_tm_item(states[3], 'b', states[3], None, RIGHT)
    tm.add_tm_item(states[3], 'c', states[4], None, RIGHT)

    tm.add_tm_item(states[4], 'c', states[4], None, RIGHT)
    tm.add_tm_item(states[4], 'd', states[5], None, RIGHT)

    tm.add_tm_item(states[5], 'd', states[5], None, RIGHT)
    tm.add_tm_item(states[5], SIGN, states[6], None, LEFT)

    tm.add_tm_item(states[6], 'a', states[6], None, LEFT)
    tm.add_tm_item(states[6], 'b', states[6], None, LEFT)
    tm.add_tm_item(states[6], 'c', states[6], None, LEFT)
    tm.add_tm_item(states[6], 'd', states[6], None, LEFT)
    tm.add_tm_item(states[6], SIGN, states[7], None, RIGHT)

    tm.add_tm_item(states[7], 'x', states[7], None, RIGHT)
    tm.add_tm_item(states[7], 'a', states[8], 'x',  RIGHT)

    tm.add_tm_item(states[8], 'y', states[8], None, RIGHT)
    tm.add_tm_item(states[8], 'a', states[8], None, RIGHT)
    tm.add_tm_item(states[8], 'b', states[9],'y', RIGHT)
    tm.add_tm_item(states[8], 'c', states[14], None, LEFT)

    tm.add_tm_item(states[9], 'z', states[9], None, RIGHT)
    tm.add_tm_item(states[9], 'b', states[9], None, RIGHT)
    tm.add_tm_item(states[9], 'c', states[10], 'z', RIGHT)
    tm.add_tm_item(states[9], 'u', states[13], None, LEFT)


    tm.add_tm_item(states[10], 'u', states[10], None, RIGHT)
    tm.add_tm_item(states[10], 'c', states[10], None, RIGHT)
    tm.add_tm_item(states[10], 'd', states[11], 'u', RIGHT)

    tm.add_tm_item(states[11], 'd', states[12], None, LEFT)
    tm.add_tm_item(states[11], SIGN, states[15], None, LEFT)

    tm.add_tm_item(states[12], 'u', states[12], None, LEFT)
    tm.add_tm_item(states[12], 'c', states[12], None, LEFT)
    tm.add_tm_item(states[12], 'z', states[9], None, RIGHT)

    tm.add_tm_item(states[13], 'z', states[13], 'c', LEFT)
    tm.add_tm_item(states[13], 'b', states[13], None, LEFT)
    tm.add_tm_item(states[13], 'y', states[8], None, RIGHT)

    tm.add_tm_item(states[14], 'y', states[14], 'b', LEFT)
    tm.add_tm_item(states[14], 'a', states[14], None, LEFT)
    tm.add_tm_item(states[14], 'x', states[7], None, RIGHT)

    tm.add_tm_item(states[15], 'u', states[15], None, LEFT)
    tm.add_tm_item(states[15], 'x', states[15], None, LEFT)
    tm.add_tm_item(states[15], 'y', states[15], None, LEFT)
    tm.add_tm_item(states[15], 'z', states[15], None, LEFT)
    tm.add_tm_item(states[15], SIGN, states[16], None, LEFT)

    # print(tm)
    # draw_TM(tm)

    input_string = input()
    tape = list(input_string)
    tape.insert(0, SIGN)
    tape.append(SIGN)
    print(tape)
    if tm.run(tape):
        print('Accept')
    else:
        print('Reject')
