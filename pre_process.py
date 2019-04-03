import torch
from torch import nn
import re
import collections
import os
import numpy as np
import phenome_classify as pc
import pandas as pd

def get_train_data(dir, dir_time):
    all_lines = np.load(dir)
    all_time = np.load(dir_time)
    train_data_list = []
    pattern = r'!|#|\$|%|\||&|;|-|\]|\^|=|~|@|\+|\[|\_'
    #get 1
    length_list = []
    for i in range(all_lines.shape[0]):
        str = all_lines[i][5]
        result = re.split(pattern, str)
        length = result[7]
        if length == "xx":
            length = "0"
        # print(length)
        length_list.append(length)
    length_list = np.array(length_list)

    #get 2
    length_list_pre = []
    for i in range(all_lines.shape[0]):
        str = all_lines[i][4]
        result = re.split(pattern, str)
        length_pre = result[7]
        if length_pre == "xx":
            length_pre = "0"
        # print(length)
        length_list_pre.append(length_pre)
    length_list_pre = np.array(length_list_pre)

    #get 3 元音0 辅音1 其他-1
    note_list = []
    first_note_class = []
    pre_class = 0
    note_phono = np.load("res/note_phono.npy")
    for i in range(all_lines.shape[0]):
        first_note_class.append(note_phono[i])
    first_note_class = np.array(first_note_class)

    #get 4
    note_pos = []
    for i in range(all_lines.shape[0]):
        str = all_lines[i][5]
        result = re.split(pattern, str)
        #print(result)
        forw = float(result[15])/100
        # backw = result[22]
        # print(length)
        #print(forw, backw)

        # pos_for = forw
        # pos_back = backw
        # pos = [pos_for, pos_back]
        note_pos.append(forw)
    note_pos = np.array(note_pos)

    #get 5、7  1->rest 0->not rest
    note_is_rest = []
    note_pre_is_rest = []
    is_rest_pre = 0
    for i in range(all_lines.shape[0]):
        str = all_lines[i][0]
        result = re.split(pattern, str)
        if pc.phonome_is_rest(str[3])==1:
            is_rest = 1
        else:
            is_rest = 0

        note_is_rest.append(is_rest)

        if i == 0:
            note_pre_is_rest.append(0)
        else:
            note_pre_is_rest.append(is_rest_pre)

        is_rest_pre = is_rest
    note_is_rest = np.array(note_is_rest)
    note_pre_is_rest = np.array(note_pre_is_rest)

    #get 6 尾辅音只有"N"
    num_coda_cons_pre_note = []
    note_num_coda = np.load("res/note_num_coda.npy")
    for i in range(all_lines.shape[0]):
        num_coda_cons_pre_note.append(note_num_coda[i])
    num_coda_cons_pre_note = np.array(num_coda_cons_pre_note)

    # see shape
    print(length_list.shape)
    print(length_list_pre.shape)
    print(first_note_class.shape)
    print(note_pos.shape)
    print(note_is_rest.shape)
    print(num_coda_cons_pre_note.shape)
    print(note_pre_is_rest.shape)

    #concat
    # length_list = length_list[:,np.newaxis]
    # length_list_pre = length_list_pre[:,np.newaxis]
    # first_note_class = first_note_class[:,np.newaxis]
    # note_pos = note_pos[:,np.newaxis]
    # note_is_rest = note_is_rest[:,np.newaxis]
    # num_coda_cons_pre_note = num_coda_cons_pre_note[:,np.newaxis]
    # note_pre_is_rest = note_pre_is_rest[:,np.newaxis]
    # trainning_data = np.concatenate((length_list, length_list_pre, first_note_class, note_pos, note_is_rest,num_coda_cons_pre_note,note_pre_is_rest),axis=1)
    # print(trainning_data.shape)
    df = pd.DataFrame({'length_list':length_list,
                       'length_list_pre':length_list_pre,
                       'first_note_class':first_note_class,
                       'note_pos':note_pos,
                       'note_is_rest': note_is_rest,
                       'num_coda_cons_pre_note':num_coda_cons_pre_note,
                       'note_pre_is_rest':note_pre_is_rest})


    dummies_field = ['length_list', 'length_list_pre', 'first_note_class']
    for each in dummies_field:
        dummies = pd.get_dummies(df[each], prefix=each, drop_first=False)
        df = pd.concat([df, dummies], axis=1)

    trainning_data = df.drop(dummies_field, axis=1)

    print(trainning_data.shape)
    print(trainning_data.keys())
    print(trainning_data)

    trainning_data = np.array(trainning_data)
    for i in range(3709):
        print(trainning_data[i])
    np.save("res/all_train.npy", trainning_data)
    # val_data = trainning_data[-500:-1,:]
    # test_data = trainning_data[-1000:-500,:]
    # trainning_data = trainning_data[:-1001,:]
    # np.save("res/trainning_data.npy",trainning_data)
    # np.save("res/val_data.npy", val_data)
    # np.save("res/test_data.npy", test_data)



if __name__ == '__main__':
    dir = "res/note_lines.npy"
    dir_time = "res/note_time.npy"
    dir_mono = "res/note_mono_lines.npy"
    get_train_data(dir, dir_time)

