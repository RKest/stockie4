# %%

from re import S
from tqdm import tqdm
from pandas import DataFrame
from data.reqesition import load_slope_sequential
from data.wrting import load_slope_model_progress
from nets.net import SlopeDirNet
from torch import Size
from dataclasses import dataclass
from typing import Tuple, List

@dataclass
class Score:
    _guess_range_tuple: Tuple[float, float]
    _n_all_guesses: int = 0
    _n_accurate_guesses: int = 0

    def register_guess(self, guess: float, is_accurate: bool):
        if self._is_in_range(guess):
            self._n_accurate_guesses += int(is_accurate)
            self._n_all_guesses += 1

    def print_acc(self):
        any_guesses = bool(self._n_all_guesses)
        if any_guesses:
            accuracy = self._n_accurate_guesses / self._n_all_guesses
            print(f"{self._guess_range_tuple} -> {self._n_accurate_guesses} / {self._n_all_guesses} = {accuracy}")
        else:
            print(f"{self._guess_range_tuple}: No guesses made")

    def _is_in_range(self, guess) -> bool:
        return self._guess_range_tuple[0] < guess <= self._guess_range_tuple[1]



scores: List[Score] = []
for i in range(10):
    scores.append(Score((i / 10, (i + 1) / 10)))


net = SlopeDirNet()
net2 = SlopeDirNet()
net = load_slope_model_progress(net, model_number=2, spec_epoch=94)
loader = load_slope_sequential(train=True, just_one=True)[0]

j, acc, rand_acc = 0, 0, 0

conf_dict = {}
conf_dict['guess'] = []
conf_dict['val'] = []


for data in tqdm(loader):
    if not data[0].size() == Size([64, 1, 102]):
        continue
    X, y = data
    out = net(X)
    out2 = net2(X)
    for i, dp in enumerate(out):
        guess = round(float(dp), 2)
        rand_guess = round(float(out2[i]), 2)
        val = int(y[i])

        is_acc = (guess > 0.5 and val == 1) or  guess <= 0.5 and val == 0
        for score in scores:
            score.register_guess(guess, is_acc)

        j+=1

        if rand_guess > 0.5 and val == 1:
            rand_acc+=1
        if rand_guess <= 0.5 and val == 0:
            rand_acc+=1

        conf_dict['guess'].append(guess)
        conf_dict['val'].append(val)

for score in scores:
    score.print_acc()

# print(acc / j)
# print(rand_acc / j)
# df = DataFrame(conf_dict)