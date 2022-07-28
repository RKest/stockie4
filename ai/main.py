import time
import numpy as np
from torch import Size
from types import SimpleNamespace
from tqdm import tqdm, trange
from constants.params import DEFAULT_MODELING_PARAMS
from constants.paths import MODELS_PATH
from data.reqesition import load_slope_sequential
from nets.training import slope_forward
from nets.optim import make_optim, make_scheduler
from nets.net import SlopeDirNet
from data.wrting import save_slope_model_progress

def big_data_slope_send_it(params=DEFAULT_MODELING_PARAMS):
    p = SimpleNamespace(**params)
    
    net = SlopeDirNet()
    optim = make_optim(net)
    sched = make_scheduler(optim, dr=0.97)

    train_loaders = load_slope_sequential(train=True)
    test_loader = load_slope_sequential()[0]
    with open(f'{MODELS_PATH}/slope-model-{p.MODEL_NUMBER}.log', 'a') as f:
        for e in trange(p.NO_EPOCHS):
            i, acc_avg, loss_avg = np.zeros(3)
            for loader in tqdm(train_loaders):
                for train in loader:
                    if not train[0].size() == Size([64, 1, 102]):
                        continue
                    i += 1
                    acc, loss = slope_forward(
                        net, optim, train, train=True)
                    acc_avg += acc
                    loss_avg += loss
                    if i % 11620 == 0:
                        j, val_acc_avg, val_loss_avg = np.zeros(3)
                        for test in test_loader:
                            if not test[0].size() == Size([64, 1, 102]):
                                continue
                            j += 1
                            val_acc, val_loss = slope_forward(
                                net, optim, test, train=False)
                            val_acc_avg += val_acc
                            val_loss_avg += float(val_loss)
                        val_acc_avg /= j
                        val_loss_avg /= j

                        acc_avg /= i
                        loss_avg /= i


                        f.write(
                            f"{p.MODEL_NAME},{round(time.time(), 3)},{e+1},{round(acc_avg, 2)},{round(loss_avg, 4)},{round(val_loss_avg, 4)},{round(val_acc_avg, 2)}\n")
                        i, acc_avg, loss_avg = np.zeros(3)
            sched.step()
            save_slope_model_progress(net, optim, sched, e, p.MODEL_NUMBER)


# def slope_send_it(net, optim, sched, params=def_params):
#     i = 0
#     p = SimpleNamespace(**params)
#     train_data = request_slope_sequential_fast(train=True, balance=True)
#     test_data = request_slope_sequential_fast(train=False, balance=False)
#     with open(f'{BASE_PATH}/slope-model-{p.MODEL_NUMBER}.log', 'a') as f:
#         for e in range(p.NO_EPOCHS):
#             for train in get_slope_data(train_data):
#                 if not train[0].size() == Size([64, 1, 102]):
#                     continue
#                 i += 1
#                 acc, loss = slope_forward(
#                     net, optim, train, train=True)
#                 if i % 100 == 0:
#                     for test in get_slope_data(test_data):
#                         val_acc, val_loss = slope_forward(
#                             net, optim, test, train=False)
#                         break
#                     f.write(
#                         f"{p.MODEL_NAME},{round(time.time(), 3)},{e+1},{round(acc, 2)},{round(float(loss), 4)},{round(float(val_loss), 4)},{round(val_acc, 2)}\n")
#             sched.step()
#             save_slope_model_progress(net, optim, sched, e, p.MODEL_NUMBER)


# def len_send_it(net, optim, sched, params=def_params):
#     i = 0
#     p = SimpleNamespace(**params)
#     train_data = request_len_sequential_fast(train=True, balance=True)
#     test_data = request_len_sequential_fast(train=False, balance=False)
#     with open(f'{BASE_PATH}/len-model-{p.MODEL_NUMBER}.log', 'a') as f:
#         for e in range(p.NO_EPOCHS):
#             for train in tqdm(get_len_data(train_data)):
#                 if not train.size() == Size([64, 1]):
#                     continue
#                 i += 1
#                 loss = len_forward(
#                     net, optim, train, train=True)
#                 if i % 100 == 0:
#                     for test in get_len_data(test_data):
#                         val_loss = len_forward(
#                             net, optim, test, train=False)
#                         break
#                     f.write(
#                         f"{p.MODEL_NAME},{round(time.time(), 3)},{e+1},{round(float(loss), 4)},{round(float(val_loss), 4)}\n")
#             sched.step()
#             save_slope_model_progress(net, optim, sched, e, p.MODEL_NUMBER)


# len_net = LenNet()
# len_optim = make_optim(len_net)
# len_sched = make_scheduler(len_optim)


if __name__ == '__main__':
    big_data_slope_send_it()
