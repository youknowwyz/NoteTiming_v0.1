import re
import collections
import os
import numpy as np
import phenome_classify as pc
import random
from collections import Counter
import sub_string as sb

def get_note_noc():
    all_lines = np.load("res/all_lines.npy")
    print(all_lines)
    pattern = r'!|#|\$|%|\||&|;|-|\]|\^|=|~|@|\+|\[|\_'
    alllen = all_lines.shape[0]
    notes = []
    for i in range(alllen):
        line_e = all_lines[i][5]
        result = re.split(pattern, line_e)
        note = result[0]
        print(note)
        notes.append(note)
    notes = np.array(notes)
    print(notes.shape)
    np.save("res/all_notes.npy", notes)

if __name__ == "__main__":
    get_note_noc()