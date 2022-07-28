import torch.optim as optim

def make_optim(net, lr=0.001):
    """Retunrs Adam for a net with a learining rate (lr)"""
    return optim.Adam(net.parameters(), lr=lr)

def make_scheduler(optimp, dr=0.75):
    """Creates scheduler for an optimiser with a decay rate (dr)"""
    return optim.lr_scheduler.ExponentialLR(optimizer=optimp, gamma=dr)