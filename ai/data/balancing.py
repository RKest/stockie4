from collections import Counter
from numpy import log
from typing import List
# from django.contrib.admin.utils import flatten
from abc import ABC, abstractmethod
import numpy as np

class Balancer(ABC):
    def __init__(self, data=None):
        if data is None:
            self.data = []
        else:
            self.data = data

    def push(self, data):
        self.data += data

    def get_data(self):
        return self.data

    def clear(self):
        self.data = []
    
    @abstractmethod
    def appraise(self, data):
        pass

# class LenBalancer(Balancer):
#     def __init__(self, data=None):
#         super(LenBalancer, self).__init__(data)

#     def appraise(self, data):
#         if not isinstance(data, list):
#             data = [data]

#         if not set(data).isdisjoint(self.data) or not self.data:
#             self.push(data)
#             return True
#         else:
#             pre_se = self.__shannons_entropy(self.data)
#             post_se = self.__shannons_entropy(self.data + [data])
#             if post_se > pre_se:
#                 self.__push_len_data(data)
#                 return True

#         return False


#     def __shannons_entropy(self, seq):
#         seq = flatten(seq)
#         n = len(seq)
#         k = len(set(seq))
#         H = -sum([ (i/n) * log((i/n)) for i in range(k)])
#         return H/log(k)

class SlopeDirBalancer(Balancer):
    def __init__(self, max_imb=50 ,data=None):
        super(SlopeDirBalancer, self).__init__(data)
        self.max_imb = max_imb
        self.__imb = 0
        self.__sign = lambda x: 1 if x > 0 else -1

    def appraise(self, data: List[List[float]], output_list) -> None:
        appriase_data = data[1][1]
        sign = self.__sign(appriase_data)
        if abs(self.__imb + sign) <= self.max_imb:
            self.__imb += sign
            final_data = [[data[0]], [int(sign == 1)]]
            output_list.append(final_data)

    def clear(self):
        self.__imb = 0