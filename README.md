# Project title

## Overview
This is a project.

## Prerequisites
- Anaconda or Miniconda
- Docker (for Docker deployment)

## Installation and Setup

### Running without Docker

1. **Clone the Repository and Navigate to Directory**
    ```bash
    cd [your-folder-path]/app
    ```

2. **Environment Setup**
    - Activate the Conda environment:
        ```bash
        conda activate myenv
        ```

3. **Launch the App**
    - Run the Streamlit application:
        ```bash
        python main.py
        ```

### Running with Docker

1. **Prepare Docker Environment**
    - Ensure Docker is installed and running on your system.

2. **Navigate to Project Directory**
    - For multiple containers:
        ```bash
        cd [path-to-app-folder-containing-docker-compose.yml]
        ```
    - For a single container:
        ```bash
        cd [path-to-app-folder-containing-Dockerfile]
        ```

3. **Build and Start the Containers**
    ```bash
    docker-compose up --build
    ```

    - The application will be accessible at `localhost:8501`.

    - Note: If you encounter issues with `pymssql`, adjust its version in `requirements.txt` or remove it before building the Docker image.

## Additional Notes
- Modify `requirements.txt` as needed for compatibility with your environment.