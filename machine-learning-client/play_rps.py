"""Module to play rock paper scissors with computer opponent, either using random outputs
or Naive Bayes classification based on player history"""

import random

# import pymongo
# import pandas
# import numpy


def play_random():
    """Randomly choose rock, paper, or scissors"""
    return random.randrange(0, 3)
