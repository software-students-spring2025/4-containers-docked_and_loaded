
![Web App Build](https://github.com/AndrewJung03/docked_and_loaded/actions/workflows/web-app.yml/badge.svg)
![ML Client Build](https://github.com/AndrewJung03/docked_and_loaded/actions/workflows/mlc.yml/badge.svg)

![Lint-free](https://github.com/nyu-software-engineering/containerized-app-exercise/actions/workflows/lint.yml/badge.svg)

## Description
The Rock-Paper-Scissors Camera Game is an interactive application that utilizes a camera to allow users to play the classic game of rock-paper-scissors against a computer opponent. The application uses computer vision to recognize hand gestures representing rock, paper, or scissors, providing a fun and engaging way for users to play the game

![Gameplay Demo](./gif/gif3.gif)

# User Stories
- As a user, I want to start the game by clicking a "Start" button so that I can begin playing rock-paper-scissors against the computer.
- As a user, I want the application to recognize my hand gestures for rock, paper, or scissors so that I can play the game without using a keyboard or mouse.\
- As a user, I want to see real-time feedback on my gesture recognition so that I can confirm that my choice has been correctly identified before the round begins.
- As a user, I want the computer to randomly select its gesture (rock, paper, or scissors) so that I can compete against it in the game.
- As a user, I want to see the results of each round (win, lose, or draw) so that I can track my performance against the computer.
- As a user, I want to see my score and the computer's score displayed on the screen so that I can keep track of who is winning throughout the game.



# Containerized App Exercise

Build a containerized app that uses machine learning. See [instructions](./instructions.md) for details.

## 🔧 Environment Setup

Each service in this project requires its own `.env` file to configure the MongoDB connection.  

Use the provided `env.example` files in each directory to create your own `.env` files:

### 1. Machine Learning Client

- Path: `machine-learning-client/.env`
- Template: `machine-learning-client/env.example`

### 2. Web App

- Path: `web-app/.env`
- Template: `web-app/env.example`