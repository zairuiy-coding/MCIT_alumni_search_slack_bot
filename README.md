# MCIT Alumni Search Slack Bot

## Set Up

We'll use a virtual environment to encapsulate all the dependencies needed for this project. This ensures consistency and avoids conflicts with system-wide packages or other projects. Once activated, you don't need to worry about installing dependencies globally.

### For Each Time You Run Your Code

Before running your code, follow these steps to ensure everything is set up correctly:

1. **Activate the Virtual Environment**:
    ```bash
    # On Windows
    venv\Scripts\activate

    # On macOS/Linux
    source venv/bin/activate
    ```

    Ensure the virtual environment is active. If your virtual environment is already activated, you will see `(venv)` at the beginning of each command line.

2. **Install All Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
    This installs all the necessary dependencies listed in `requirements.txt`.

### If You Want to Install a New Package

When you need to add a new package to the project, follow these steps:

1. **Activate the Virtual Environment**:
    ```bash
    # On Windows
    venv\Scripts\activate

    # On macOS/Linux
    source venv/bin/activate
    ```

2. **Install the New Package**:
    ```bash
    pip install <package-name>
    ```

3. **Update `requirements.txt`**:
    ```bash
    pip freeze > requirements.txt
    ```
    This updates `requirements.txt` to include the new package, ensuring others can install it using the file.

By following these instructions, we can ensure a consistent and conflict-free development environment for our project.
