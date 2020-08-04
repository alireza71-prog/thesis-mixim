import numpy as np


def sample_from_exp_dist(rate):
    return round(np.random.exponential(rate, None), 2)