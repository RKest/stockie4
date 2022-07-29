from os import listdir
import time

from constants.paths import MODELS_PATH

def get_next_model_number(path=MODELS_PATH):
    """Returns next model number for training, 
    in order to distinguish between different training runs"""
    model_paths = listdir(path)
    if not len(model_paths):
        return 1
    model_numbers = [int(model_path.split('.')[0].split('-')[-1]) for model_path in model_paths]
    return max(model_numbers) + 1

MODEL_NAME = f"stockieAI-{int(time.time())}"

DEFAULT_MODELING_PARAMS = {
    'MODEL_NUMBER': get_next_model_number(),
    'MODEL_NAME': MODEL_NAME,
    'NO_EPOCHS': 100
}

DEFAULT_TRAIN_PARAMS = {
    'batch_size': 64,
    'shuffle': True,
    'num_workers': 6
}

