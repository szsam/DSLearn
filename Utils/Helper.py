import re

import termcolor
import numpy as np


def debug(info):
    print(termcolor.colored(info, "red"))


def analysis(data):
    data = np.array(data)
    mean = data.mean()
    var = np.var(data)
    return mean, var

def splitSentence(sentence):
    return re.split(r"([!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~\s+])", sentence)