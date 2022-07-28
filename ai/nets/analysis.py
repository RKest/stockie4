from numpy import array
from numpy import sum as nsum
from numpy import round as nround

def score_slope(out, y):
    out, y = out.tolist(), y.tolist()
    out, y = array(out), array(y)
    direc_right = nsum(nround(out) == y)
    direc_right /= len(out)
    return direc_right
