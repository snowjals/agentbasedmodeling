import numpy as np
import termcolor
import re


def cprint(s):
    '''
    Example usage:
    cprint('[y]Hello [g]world[r]!!!')
    cprint('this text is in [r]red, and this is [y]yellow :)')
    '''
    C = {'r': 'red',
         'g': 'green',
         'b': 'blue',
         'y': 'yellow',
         'm': 'magenta',
         'c': 'cyan',
         'w': 'white'}
    L = re.split('(\[\w\])', s)  # noqa
    color = 'white'

    s_colored = []
    for each in L:
        if re.match('\[\w\]', each):  # noqa
            color = C[each[1]]
        else:
            s_colored.append(termcolor.colored(each, color))

    print(''.join(s_colored))


def sigmoid(x):
    return 1 / (1 + np.exp(x))


def biased_bernoulli(p_true):
    return np.random.choice([1, 0], p=(p_true, 1-p_true))


