# %%

from tqdm import tqdm
from pandas import DataFrame
from data.reqesition import load_slope_sequential
from data.wrting import load_slope_model_progress
from nets.net import SlopeDirNet
from torch import Size

net = SlopeDirNet()
net2 = SlopeDirNet()
net = load_slope_model_progress(net, model_number=9, spec_epoch=68)
loader = load_slope_sequential(train=False)[0]

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

        j+=1
        if guess > 0.5 and val == 1:
            acc+=1
        if guess <= 0.5 and val == 0:
            acc+=1

        
        if rand_guess > 0.5 and val == 1:
            rand_acc+=1
        if rand_guess <= 0.5 and val == 0:
            rand_acc+=1

        conf_dict['guess'].append(guess)
        conf_dict['val'].append(val)
print(acc / j)
print(rand_acc / j)
df = DataFrame(conf_dict)
df.to_csv('guesses.csv', sep=';')

# %%