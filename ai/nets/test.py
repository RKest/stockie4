from torch import no_grad
def test_net(net, test):
    with no_grad():
        for t in test:
            X, y = t
            out = net(X)
            return out, y

