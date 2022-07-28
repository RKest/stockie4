import json
from math import floor
from numba import njit
import numpy as np
from constants.paths import TEST_DATA_PATH, TEST_DATA_PATH_UNPREPED, TRAIN_DATA_PATH, TRAIN_DATA_PATH_UNPREPED

f_train = open(TRAIN_DATA_PATH_UNPREPED, "r")
train_json = json.loads(f_train.read())
train_json = [np.array(j, dtype=float) for j in train_json]
train_json_len = len(train_json)
f_train.close()

f_test = open(TEST_DATA_PATH_UNPREPED, "r")
test_json = json.loads(f_test.read())
test_json = [np.array(j, dtype=float) for j in test_json]
test_json_len = len(test_json)
f_test.close()

def save_slope_sequential(train=False, single_loader_len=15000):
    i, j = 0, 0
    __json = train_json if train else test_json
    __save = TRAIN_DATA_PATH if train else TEST_DATA_PATH
    __json_len = len(__json)
    with open(__save, 'a') as f:
        while i < __json_len:
            data = []
            while j < single_loader_len and i < __json_len:
                x = __json[i]
                i += 1
                j += 1
                x = vectorise_data_fast(x)
                x = compress_vec_arr_fast(x)
                data.append(x.tolist())
            print(f'{__file__}: {i // single_loader_len}/{floor(__json_len/single_loader_len)}')
            f.write(str(data))
            f.write('\n')
            data = []
            j = 0

@njit
def vectorise_data_fast(data, min_vec_len=5, prec_frac=10):
    global_i, local_i = 0, 0
    vectors = []
    tmp_vec = np.zeros(4000)

    data_len = len(data)
    std = np.std(data)
    prec = std / prec_frac

    while global_i < data_len:
        if local_i <= min_vec_len:
            tmp_vec[local_i] = data[global_i]
            local_i += 1
            global_i += 1
        elif abs(aprox_vec_el(tmp_vec[:min_vec_len], local_i - min_vec_len + 1) - data[global_i]) > prec:
            vectors.append(tmp_vec[:local_i].copy())
            local_i = 0
        else:
            tmp_vec[local_i] = data[global_i]
            local_i += 1
            global_i += 1

    if local_i >= min_vec_len:
        vectors.append(tmp_vec[:local_i].copy())

    return vectors

@njit
def aprox_vec_el(arr, i):
    first = arr[0]
    last = arr[-1]
    return last + ((last - first) / (len(arr) -1)) * i

@njit
def compress_vec_arr_fast(vec_arr):
    ret_arr = np.zeros((len(vec_arr), 3))
    for i in range(len(vec_arr)):
        ret_arr[i][0] = vec_arr[i][0]
        ret_arr[i][1] = vec_arr[i][-1]
        ret_arr[i][2] = len(vec_arr[i])
    return ret_arr