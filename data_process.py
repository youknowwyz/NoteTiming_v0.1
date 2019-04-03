import re
import collections
import os
import numpy as np
import phenome_classify as pc
import sub_string as sb


def read_data():
    pattern = r'!|#|\$|%|\||&|;|-|\]|\^|=|~|@|\+|\[|\_'

    # all_time = np.load("res/no_cl_time.npy")
    # all_lines = np.load("res/no_cl_lines.npy")
    # all_mono_lines = np.load("res/no_cl_mono_lines.npy")

    all_time = np.load("res/all_time.npy")
    all_lines = np.load("res/all_lines.npy")
    all_mono_lines = np.load("res/all_mono_lines.npy")
    all_notes = np.load("res/all_notes.npy")

    len_all = all_time.shape[0]
    print(all_time.shape)
    print(all_lines.shape)
    print(all_mono_lines.shape)
    timenow = "-9999"

    note_time = []
    note_lines = []
    note_mono_lines = []
    note_phono = []
    note_notes = []
    note_num_coda = []
    #print(all_mono_lines)
    # note = "0"
    # note_now = "0"
    # exist_nuc = False
    first_phono = []
    num_coda = []
    #### CALC 条件3
    for i in range(len_all - 1):
        if all_time[i][0] == all_time[i + 1][0]:
            first_phono.append(1)
        elif pc.phonome_classify(all_time[i][0]) == -1:
            first_phono.append(-1)
        else:
            if all_mono_lines[i][2] == "N\n":
                first_phono.append(1)
            else:
                first_phono.append(0)

    first_phono.append(-1)
    first_phono = np.array(first_phono)
    print(first_phono.shape)

    ####CALC 条件6
    for i in range(all_lines.shape[0]):
        str = all_lines[i][0]
        result = re.split(pattern, str)
        pre_note = result[2]
        if pre_note == "N":
            num_coda.append(1)
        else:
            num_coda.append(0)

    num_coda = np.array(num_coda)
    print(num_coda.shape)

    for i in range(len_all-1):
        if all_time[i][0] != all_time[i+1][0]:
            note_time.append(all_time[i])
            note_lines.append(all_lines[i])
            note_mono_lines.append(all_mono_lines[i])
            note_phono.append(first_phono[i])
            note_num_coda.append(num_coda[i])

        # NOTE IN PITCH
        #
        # note = all_notes[i]
        # if note == note_now and exist_nuc == True:
        #     continue
        # if note != note_now:
        #     exist_nuc = False
        #
        # if pc.phonome_classify(all_mono_lines[i][2].split("\n")[0]) == 0:
        #     exist_nuc = True
        #     note_time.append(all_time[i])
        #     note_lines.append(all_lines[i])
        #     note_mono_lines.append(all_mono_lines[i])
        #     note_notes.append(all_notes[i])
        #
        # note_now = note



    note_time = np.array(note_time)
    note_lines = np.array(note_lines)
    note_mono_lines = np.array(note_mono_lines)
    note_phono = np.array(note_phono)
    # note_notes = np.array(note_notes)
    note_num_coda = np.array(note_num_coda)

    print(note_time.shape)
    print(note_lines.shape)
    print(note_mono_lines.shape)
    print(note_phono.shape)
    print(note_num_coda.shape)
    # print(note_notes.shape)
    # for i in range(note_num_coda.shape[0]):
    #     print(note_num_coda[i])
    np.save("res/note_time.npy", note_time)
    np.save("res/note_lines.npy", note_lines)
    np.save("res/note_mono_lines.npy", note_mono_lines)
    np.save("res/note_notes.npy", note_notes)
    np.save("res/note_phono.npy", note_phono)
    np.save("res/note_num_coda.npy", note_num_coda)
    # np.save("res/no_time.npy", note_time)
    # np.save("res/no_lines.npy", note_lines)
    # np.save("res/no_mono_lines.npy", note_mono_lines)



if __name__ == '__main__':
    read_data()