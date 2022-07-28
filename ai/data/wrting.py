from constants.params import DEFAULT_MODELING_PARAMS
from constants.paths import CPS_PATH, MODELS_PATH
from torch import save, load
from json import loads
from os import listdir


def save_len_model_progress(net, optim, sched, epoch, model_number, path=CPS_PATH, params=DEFAULT_MODELING_PARAMS):
    epoch = epoch + 1
    with open(f'{path}/len-params.json', 'w') as f: 
        f.write(f'{{\n\t"currEpoch": {epoch}\n}}')

    model_id = f'{model_number}-{epoch}'
    save(net.state_dict(), f'{path}/ln{model_id}.pt')
    save(optim.state_dict(), f'{path}/lo{model_id}.pt')
    save(sched.state_dict(), f'{path}/ls{model_id}.pt')

def load_len_model_progress(net, optim, sched, model_number, path=CPS_PATH, params=DEFAULT_MODELING_PARAMS):
    with open(f'{path}/len-params.json', 'r') as f:
        json_params = loads(f.read())
        latest_epoch = json_params['currEpoch']
        params['NO_EPOCHS'] -= int(latest_epoch)
    
    model_id = f'{model_number}-{latest_epoch}'
    net.load_state_dict(load(f'{path}/ln{model_id}.pt'))
    optim.load_state_dict(load(f'{path}/lo{model_id}.pt'))
    sched.load_state_dict(load(f'{path}/ls{model_id}.pt'))

    return net, optim, sched

def save_slope_model_progress(net, optim, sched, epoch, model_number, path=CPS_PATH):
    epoch = epoch + 1
    with open(f'{path}/slope-params.json', 'w') as f: 
        f.write(f'{{\n\t"currEpoch": {epoch}\n}}')

    model_id = f'{model_number}-{epoch}'
    save(net.state_dict(), f'{path}/sn{model_id}.pt')
    save(optim.state_dict(), f'{path}/so{model_id}.pt')
    save(sched.state_dict(), f'{path}/ss{model_id}.pt')

def load_slope_model_progress(net, optim=None, sched=None, model_number=1, spec_epoch=-1, path=CPS_PATH, params=DEFAULT_MODELING_PARAMS):
    if spec_epoch == -1:
        with open(f'{path}/slope-params.json', 'r') as f:
            json_params = loads(f.read())
            latest_epoch = json_params['currEpoch']
            params['NO_EPOCHS'] -= int(latest_epoch)
    else:
        latest_epoch = spec_epoch

    model_id = f'{model_number}-{latest_epoch}'

    net.load_state_dict(load(f'{path}/sn{model_id}.pt'))
    if optim is not None:
        optim.load_state_dict(load(f'{path}/so{model_id}.pt'))
    if sched is not None:
        sched.load_state_dict(load(f'{path}/ss{model_id}.pt'))

    if optim is None and sched is None:
        return net
    if optim is None:
        return net, sched
    if sched is None:
        return net, optim
    return net, optim, sched
