from nets.analysis import score_slope
import torch.nn.functional as F
from torch import no_grad


def slope_forward(net, optim, data, train=False):
    X, y = data
    y = y.view(64,1,1)
    if train:
        net.zero_grad()
        out = net(X)
        loss = F.mse_loss(out, y)
    else:
        with no_grad():
            out = net(X)
            loss = F.mse_loss(out, y)
    
    if train:
        loss.backward()
        optim.step()

    acc = score_slope(out, y)
    det_loss = float(loss.detach())
    return acc, det_loss


def len_forward(net, optim, data, train=False):
    X, y = data
    if train:
        net.zero_grad()
        out = net(X)
        loss = F.l1_loss(out, y)
    else:
        with no_grad():
            out = net(X)
            loss = F.l1_loss(out, y)
    
    if train:
        loss.backward()
        optim.step()

    return loss