# %%
import json
from typing import List
from random import randint

from tqdm import tqdm
from constants.paths import DATA_PATH, TEST_DATA_PATH, TRAIN_DATA_PATH
from data.tensorisation import tensorise_data_fast
from data.balancing import SlopeDirBalancer
from numba import njit
import numpy as np

s_balancer = SlopeDirBalancer()

@njit
def get_data_slices(c_vec_arr, slice_len=51, slices_amount=3):
    return_arr = []
    if len(c_vec_arr) < slice_len:
        return return_arr
    for i in range(slices_amount):
        r = randint(0, len(c_vec_arr) - slice_len)
        return_arr.append(c_vec_arr[r:r+slice_len])
    return return_arr

@njit
def get_all_data_slices(c_vec_arr: np.ndarray, slice_len=51) -> np.ndarray:
    if len(c_vec_arr) < slice_len:
        return None 
    return_arr = np.zeros((len(c_vec_arr) - slice_len, slice_len, 3))
    for i in range(len(c_vec_arr) - slice_len):
        return_arr[i] = c_vec_arr[i:i+slice_len]
    return return_arr


def load_slope_sequential(train=False):
    loader_list = []
    path = TRAIN_DATA_PATH if train else TEST_DATA_PATH
    with open(path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            data = []
            x: List[List[List[float]]] = json.loads(line)
            for xp in tqdm(x):
                xp = np.array(xp)
                xp = get_all_data_slices(xp)
                if xp is None:
                    continue
                for xpp in xp:
                    xpp = make_training_data(xpp)
                    s_balancer.appraise(xpp, data)

            data = tensorise_data_fast(data)
            loader_list.append(data)
            s_balancer.clear()
            data = []
    return loader_list

# def save_slope_sequential(train=False, single_loader_len=2000):
#     i, j, data = 0, 0, []
#     __json = train_json if train else test_json
#     __save = __SAVED_SLOPE_PATH if train else __SAVED_SLOPE_TEST_PATH
#     __json_len = len(__json)
#     with open(__save, 'a') as f:
#         while i < __json_len:
#             while j < single_loader_len and i < __json_len:
#                 x = __json[i]
#                 i+=1
#                 j+=1
#                 x = vectorise_data_fast(x)
#                 x = compress_vec_arr_fast(x)
#                 data.append(x.tolist())
#             print(f'{i/single_loader_len}/{floor(__json_len/single_loader_len)}')
#             f.write(str(data))
#             f.write('\n')
#             data = []
#             j = 0


def request_pre_balanced_data():
    with open(f'{DATA_PATH}/_data.json', 'r') as f:
        data = f.read()
        data = json.loads(data)
        return data

@njit
def make_training_data(c_data_arr: np.ndarray) -> List[List[float]]:
    test_vec = c_data_arr[-1]
    train_vecs = c_data_arr[:-1]

    train_tensor_data, test_tensor_data = [], []

    test_len = test_vec[2]

    test_slope = (test_vec[1] - test_vec[0]) / (test_len - 1)
    train_trigger = test_vec[0]

    for j in range(len(train_vecs)):
        vec = train_vecs[j]
        if j == 0:
            train_tensor_data.append(vec[0])
            train_tensor_data.append(vec[1])
            train_tensor_data.append(vec[2])
        else:
            train_tensor_data.append(vec[1])
            train_tensor_data.append(vec[2] + 1)

    train_tensor_data.append(train_trigger)
    test_tensor_data.append(test_len)
    test_tensor_data.append(test_slope)
    return [train_tensor_data, test_tensor_data]

@njit
def vectorise_data_fast(data, min_vec_len=5, prec_frac=10):
    global_i, local_i = 0, 0
    vectors = []
    tmp_vec = np.zeros(1000)

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
