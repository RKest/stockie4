import torch
import numpy as np
from numba import njit
from constants.params import DEFAULT_TRAIN_PARAMS

class Dataset(torch.utils.data.Dataset):
    def __init__(self, data, results):
        self.data = data
        self.results = results
    def __len__(self):
        return len(self.data)
    def __getitem__(self, inx):
        X = torch.Tensor(self.data[inx])
        y = torch.Tensor(self.results[inx])
        return X, y


def tensorise_data(data, params=DEFAULT_TRAIN_PARAMS):
    ds = Dataset(np.array([d[0] for d in data]), np.array([d[1] for d in data]))
    sampler = torch.utils.data.RandomSampler(data_source=ds)
    return torch.utils.data.DataLoader(ds, **params, sampler=sampler)

tensorise_data_fast = njit()(tensorise_data)