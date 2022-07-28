import numpy as np

def aprox_vec_el(arr, i):
    first = arr[0]
    last = arr[-1]
    return last + ((last - first) / (len(arr) -1)) * i

def vectorise_data(data, min_vec_len=5, precision_frac=10):
    vectors = []
    tmp_vector = []

    data = np.array(data)
    std = np.std(data)
    precision = std / precision_frac

    for i in range(len(data)):
        if len(tmp_vector) > min_vec_len and abs(aprox_vec_el(tmp_vector[:min_vec_len], len(tmp_vector) - min_vec_len) - data[i-1]) > precision:
            tmp = tmp_vector[-1]
            tmp_vector = tmp_vector[:-1]
            vectors.append(tmp_vector)
            tmp_vector = [tmp]
        tmp_vector.append(data[i])
    if len(tmp_vector) > min_vec_len:
        vectors.append(tmp_vector)

    return vectors



def compress_vec_arr(vec_arr):
    return [[vec[0], vec[-1], len(vec)] for vec in vec_arr]

def fill_vector(start, end, leng):
    return [start + ((end - start) / (leng - 1) * i) for i in range(leng)]


