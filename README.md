# MCIT Alumni Search Slack Bot

## Reminder: Work on your own branch & activate venv each time

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

## Git Workflow

To ensure a smooth and efficient workflow, please follow these Git guidelines when working on the project:

1. **Clone the Repository**:
    ```bash
    git clone <repository-url>
    ```
    This clones the project repository to your local machine.

2. **Create and Switch to a New Branch**:
    ```bash
    git checkout -b <branch-name>
    ```
    This creates a new branch and switches to it. Follow a naming convention like "name_feature" (e.g. "zairuiy_commands")

3. **Pull the Latest Changes**:
    ```bash
    git pull origin main
    ```
    If you are on the main branch, before starting your work, always pull the latest changes from the main branch to ensure your branch is up to date.

4. **Check the Status of Your Repository**:
    ```bash
    git status
    ```
    This shows the status of your working directory and staging area, indicating any changes.

5. **Add Changes to Staging**:
    ```bash
    git add <file-name>
    ```
    or add all changes:
    ```bash
    git add .
    ```

6. **Commit Your Changes**:
    ```bash
    git commit -m "Descriptive commit message"
    ```
    Provide a clear and concise commit message describing your changes.

7. **Push Your Changes to the Remote Repository**:
    ```bash
    git push origin <branch-name>
    ```

8. **Create a Pull Request**:
    After pushing your changes, create a pull request on the repository's GitHub page to merge your changes into the main branch.

## Running the Flask App with Celery

### 1. Install Required Dependencies

Ensure you have installed all required dependencies by running:

```bash
pip install -r requirements.txt
```

### 2. Start the Redis Server

Make sure that Redis is running on your local machine. You can start the Redis server with:

```bash
redis-server
```

### 3. Start the Celery Worker

In a new terminal, navigate to your project directory and start the Celery worker:

```bash
celery -A bot.celery worker --loglevel=info
```

- `-A bot.celery`: This specifies that Celery should be initialized using the Celery instance defined in the `bot/__init__.py`.

- `--loglevel=info`: This sets the logging level to `info`, which provides a good balance of useful output and avoiding too much verbosity.

### 4. Start the Flask Application

In another terminal window, start your Flask app:

```bash
python app.py
```

Your app will now be running at http://localhost:3000 and should be able to handle requests, including those routed through Celery.

### 5. Stopping the Services

When you're done testing or using the app:

- Stop the Flask application with Ctrl + C.
- Stop the Celery worker by finding its process (`ps aux | grep 'celery'`) and killing it (`kill -9 <pid>`).
- Optionally, stop the Redis server with Ctrl + C in the terminal where it’s running