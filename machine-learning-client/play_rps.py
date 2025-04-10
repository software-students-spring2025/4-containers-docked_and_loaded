"""Module to play rock paper scissors with computer opponent, either using random outputs
or Naive Bayes classification based on player history"""

import random
import os
from collections import Counter
from pymongo import MongoClient


def play_random():
    """Randomly choose rock, paper, or scissors"""
    return random.randrange(1, 4)


def get_conditionals(last_played, history):
    """Get conditional probabilities of next move given last move played"""
    counts = {1: {1: 0, 2: 0, 3: 0}, 2: {1: 0, 2: 0, 3: 0}, 3: {1: 0, 2: 0, 3: 0}}
    for i in range(len(history) - 1):
        counts[history[i]][history[i + 1]] += 1
    return counts[last_played]


def predict(last_played, conditionals, counts, total_games):
    """Predict the best possible move based on opponent's previous moves"""
    prob_rock = counts[1] / total_games
    prob_paper = counts[2] / total_games
    prob_scissors = counts[3] / total_games

    conditional_rock = conditionals[1] / counts[last_played]
    conditional_paper = conditionals[2] / counts[last_played]
    conditional_scissors = conditionals[3] / counts[last_played]

    rock = prob_rock * conditional_rock
    paper = prob_paper * conditional_paper
    scissors = prob_scissors * conditional_scissors

    best_option = max(rock, paper, scissors)

    if best_option == rock:
        return 1

    if best_option == paper:
        return 2

    if best_option == scissors:
        return 3

    return play_random()


def play_nb(user):
    """Play based off of the user's history using Naive Bayes classifier"""
    client = MongoClient(os.getenv("MONGO_URI"))
    db = client[os.getenv("DB_NAME")]
    collection = db["users"]

    user = collection.find_one({"username": user})
    user_history = user["history"]

    if not user_history:
        return play_random()

    last_played = user_history[-1]
    total_games = len(user_history)
    counts = Counter(user_history)
    conditionals = get_conditionals(last_played, user_history)

    return predict(last_played, conditionals, counts, total_games)
