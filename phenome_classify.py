import re
import collections
import os
import numpy as np

#cl是两个一样的音后面附加的 不发音 N不发音 br不发音
def phonome_classify(str):
    vowel = ['a', 'i', 'u', 'e', 'o']
    other = ['br', 'sil', 'pau', 'cl']

    if str in vowel:
        return 0
    elif str in other:
        return -1
    else:
        return 1

def phonome_is_rest(str):
    rest = ['br', 'sil', 'pau', 'cl']
    if str in rest:
        return 1
    else:
        return 0

def get_phonome_list(dir):
    all_lines = np.load(dir)
    phenome_list = []
    pattern = r'!|#|\$|%|\||&|;|-|\]|\^|=|~|@|\+|_'
    for i in range(all_lines.shape[0]):
        str = all_lines[i][0]
        result = re.split(pattern, str)
        phenome = result[3]
        print(phenome)
        if phenome != 'sil':
            flag = phonome_classify(phenome)
            phenome_list.append(flag)
        else:
            phenome_list.append('sil')
    return phenome_list

def check_phenome(dir):
    all_lines = np.load(dir)
    phenome_list = []
    counter_c = collections.Counter()
    pattern = r'!|#|\$|%|\||&|;|-|\]|\^|=|~|@|\+|_'
    for i in range(all_lines.shape[0]):
        str = all_lines[i][0]
        result = re.split(pattern, str)
        phenome = result[3]
        print(phenome)
        counter_c[phenome] = 1

    print(counter_c.keys())

if __name__ == '__main__':
    #phonome_list = get_phonome_list("res/all_lines.npy")
    check_phenome("res/all_lines.npy")
