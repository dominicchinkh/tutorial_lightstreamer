# Project Setup Guide

This guide walks you through setting up a local Python virtual environment and installing the required dependencies for this project.

## ⚙️ Prerequisites

Before you begin, ensure you have Python 3 installed on your system. You can verify your Python version by running:

```bash
python3 --version
```

## 🚀 Setup Instructions

Follow these three steps to get your environment ready:

### 1. Create the Environment

Utilize Python's built-in `venv` module to create an isolated virtual environment. This prevents dependency conflicts with other projects on your system.

```bash
python3 -m venv .venv
```

### 2. Activate the Environment

You must activate the virtual environment before installing packages. Run the following command in your terminal:

```bash
source .venv/bin/activate
```

💡 Tip: Once activated, your terminal prompt will be prefixed with `(.venv)`, indicating that any subsequent Python or pip commands will run strictly within this isolated environment.

### 3. Install Dependencies

With the environment activated, install the `lightstreamer-client-lib` and `requests` libraries using pip:

```bash
python -m pip install lightstreamer-client-lib
python -m pip install requests
```

## 🏃‍♂️ Run the Application

Once the dependencies are installed, you can execute the main script by running:

```bash
python main.py
```

## 🛑 Deactivating the Environment

When you are finished working on the project and want to return to your global system Python environment, simply run:

```bash
deactivate
```