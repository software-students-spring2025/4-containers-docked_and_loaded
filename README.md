![Lint-free](https://github.com/nyu-software-engineering/containerized-app-exercise/actions/workflows/lint.yml/badge.svg)

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