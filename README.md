# The Game Of Life

## 📄 Overview


🏡 This project implements an interactive version of the classic simulation game, *John Conway's Game of Life*, using Pygame. The game allows users to select different starting patterns from classic configurations (like the *glider*, *small exploder*, and others) stored in a JSON file. A user-friendly interface lets users preview and choose their preferred configuration before launching the simulation.

🤔 The game's objective is to simulate the evolution of cells on a grid based on simple rules, which lead to complex and intriguing patterns. This project goes beyond simple simulation by offering a graphical interface where each user can select their starting pattern. This customization allows a better understanding of specific behaviors in each configuration, making the experience both educational and enjoyable.

This project is ideal for beginners in graphical programming with Python and for those interested in cellular automaton simulations. In addition to serving as a learning tool, the code is designed to be easily extensible, allowing the addition of new patterns or features, such as speed control and tracking initial configuration history.

🌐 Access the app and start your exploration now at [@Not implemented yet](https://wikipedia.com).

### Game Rules
Conway's Game of Life is a cellular automation method created by John Conway. Originally inspired by biological concepts, this game has been applied in various fields such as graphics, terrain generation, and more.

The "game" is a zero-player game, meaning its evolution is determined by its initial state and requires no further input. One interacts with the Game of Life by creating an initial configuration and observing how it evolves, or, for "advanced players," by creating patterns with specific properties.

Since the Game of Life is structured on a grid of nine cells, each cell has eight neighboring cells, as shown in the provided figure. A given cell (i, j) in the simulation can be accessed on a grid [i][j], where i and j are the row and column indices, respectively. The value of a given cell at any moment depends on the state of its neighbors in the previous time step. Conway's Game of Life has four rules:

- If a cell is ON and has fewer than two ON neighbors, it turns OFF.
- If a cell is ON and has two or three neighbors that are ON, it remains ON.
- If a cell is ON and has more than three neighbors that are ON, it turns OFF.
- If a cell is OFF and has exactly three neighboring cells that are ON, it becomes ON.

![Image1](images/image1.png)

## Prerequisites

- **Anaconda or Miniconda**: For easy environment management
- **Docker** (optional): To run the app in a containerized setup

## ⚙️ Installation and Setup

### Requirements
- **Python 3.11**
- **Python Libraries**: Managed with `poetry`

## 🛠️ Quick Start Guide

### Option 1: Run the App without Docker

#### Step 1: Set Up Your Environment

1. **Clone the repository**:
    ```bash
    git clone https://github.com/LudovicGardy/game_of_life
    cd game_of_life
    ```

2. **Create and Activate a Virtual Environment**:
   - **Using Conda** (recommended):
       ```bash
       conda create -n myenv python=3.11
       conda activate myenv
       ```

   - **Using a Python Virtual Environment**:
       ```bash
       python3 -m venv .venv
       source .venv/bin/activate
       ```

#### Step 2: Install Dependencies with Poetry

- Once the environment is active, install dependencies:
    ```bash
    poetry install --no-root
    ```

#### Step 3: Run the Application

- **To run the full application**:
    ```bash
    python run/main.py
    ```

- **To run a simplified version**:
    ```bash
    cd simple_version
    python run/main.py
    ```

### Option 2: Run the App with Docker

#### Step 1: Set Up Docker Environment

- Make sure **Docker** is installed and running on your system.

#### Step 2: Navigate to the Correct Directory

- **For a multi-container setup**:
    ```bash
    cd [path-to-app-folder-with-docker-compose.yml]
    ```

- **For a single container**:
    ```bash
    cd [path-to-app-folder-with-Dockerfile]
    ```

#### Step 3: Build and Start the Containers

- Run the following command to build and launch the app in Docker:
    ```bash
    docker-compose up --build
    ```

- **Access the Application**:
    - Open your browser and go to `http://localhost:8501`.

- **Troubleshooting**:
    - If there’s an issue with `pymssql`, try adjusting its version in `requirements.txt` or temporarily removing it.

## 👤 Author

- **LinkedIn**: [Ludovic Gardy](https://www.linkedin.com/in/ludovic-gardy/)
- **Website**: [https://www.sotisanalytics.com](https://www.sotisanalytics.com)
