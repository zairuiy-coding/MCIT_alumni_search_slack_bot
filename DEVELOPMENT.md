# Development Guidelines

## Setting Up Your Development Environment

This guide provides step-by-step instructions for setting up your development environment, managing dependencies, and following the correct workflow when contributing to the project.

### 1. Clone the Repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/yourusername/MCIT_Alumni_Search_Slack_Bot.git
cd MCIT_Alumni_Search_Slack_Bot
```

### 2. Create and Activate a Virtual Environment

To avoid dependency conflicts, it's recommended to work within a virtual environment.

#### Create the virtual environment:

```bash
python3 -m venv venv
```

#### Activate the virtual environment:

-   **macOS/Linux:**
	   ``` bash
	   source venv/bin/activate
	```
-   **Windows:**
	```bash
	venv\Scripts\activate
	```
### 3. Install Dependencies

With the virtual environment activated, install the required dependencies:
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a  `.env`  file in the root directory of the project with the following content:

```bash
OPENAI_API_KEY=your_openai_api_key
SLACK_BOT_TOKEN=your_slack_bot_token
SLACK_SIGNING_SECRET=your_slack_signing_secret
DATABASE_URL=your_postgresql_database_url
REDIS_URL=redis://localhost:6379/0
```
Ensure that all necessary environment variables are included and correctly set.

### 5. Database Setup

Ensure that PostgreSQL is installed and running on your local machine. You should:

-   Create the database as specified in  `DATABASE_URL`.
-   Migrate any necessary schema or data to this database.

For more detailed instruction on migrating data into the database, please check our [Database Documentation](https://docs.google.com/document/d/1uKjry16lbN22__4PVICnrkDwjMbquW5R_q-iX836c2o/edit).


### 6. Start Redis

Redis must be running for the application to work properly, as it’s used both as a session store and for managing Celery tasks. However, before starting a new Redis instance, it’s a good practice to check if Redis is already running on your machine to avoid starting duplicate instances.

#### 6.1 Check if Redis is Already Running

To check if Redis is running, use the following command:

```bash
ps aux | grep redis-server
```
This command will display any running Redis instances. Look for lines that mention `redis-server` to identify active Redis processes.

#### 6.2 Start Redis

If Redis is not running, you can start it with:
```bash
redis-server
```

#### 6.3 Managing Redis Instances

If you find that multiple Redis instances are running and you wish to stop a specific instance, you can do so by finding the process ID (PID) and then killing it.

1.  **Find the PID**:
    
    -   The  `ps aux | grep redis-server`  command will also show the PID (usually the second column).
2.  **Kill the Process**:
    
    -   To stop a specific Redis instance, use:
	    ```bash
	    kill <PID>
		``` 
		Replace `<PID>` with the actual process ID.
	
3. **Force Kill (if necessary)**:

-   If the process doesn’t stop with the normal  `kill`  command, you can force it to stop with:
	```bash
	kill -9 <PID>
	```
	Make sure to use the kill commands with caution, as terminating the wrong process might affect other services on your machine.

### 7. Running and Testing Locally

To test the app locally, you'll need to expose your local server to the internet using a tool like **ngrok**. This is necessary because Slack's events API requires a public URL to send events to your bot.

#### 7.1 Set Up Ngrok

-   Install ngrok from the  [official website](https://ngrok.com/).
-   Start ngrok on the port your Flask app is running on (usually  `5000`):
    
    ```bash
    ngrok http 5000
    ```
#### 7.2 Configure Slack

-   Go to your Slack app settings and update the  **Request URL**  for the Slack events and commands to the ngrok URL you copied, followed by the appropriate endpoint (e.g.,  `https://your-ngrok-url.ngrok.io/slack/events`).

#### 7.3 Run the Flask App

-   Start your Flask app locally:
	```bash
	python  app.py
	```

#### 7.4 Start the Celery Worker

In a new terminal window:

``` bash
celery  -A  bot.celery  worker  --loglevel=info
```

### 8. Deploying Code Updates to Heroku

Whenever you have updates to your code that you'd like to deploy to Heroku, follow these steps:

#### 8.1 Commit Your Changes

-   Ensure that all your changes are committed to your local Git repository:
    
    ```bash
    git add .
	git commit -m "Your commit message"
	```
#### 8.2 Push to Heroku

-   Push your changes to the Heroku remote repository:
    
    ```bash
    git push heroku your-branch-name
    ```

#### 8.3 Monitor the Deployment

-   You can monitor the deployment process using:
   
	```bash
	Heroku logs --tail
	```

### 9. Git Workflow

#### 9.1 Working on a New Feature or Bugfix

1.  **Create a New Branch**:
    ```bash
    git checkout -b your-branch-name
	```
2. **Make Your Changes**: Edit the files and commit your changes.
3. **Push Your Changes**:
    ```bash
    git push origin your-branch-name
	```
4. **Create a Pull Request**: Submit a pull request through GitHub to merge your branch into `main`.

#### 9.2 Keeping Your Branch Updated

Before submitting your pull request, ensure your branch is up-to-date with  `main`:
```bash
git pull origin main
```

### 10. Stopping Services

Once you are done working:

-   Stop the Flask app using  `Ctrl + C`.
-   Stop the Celery worker by identifying and killing the process.
-   Optionally, stop the Redis server.

### Troubleshooting

#### Common Issues and Solutions

1.  **Virtual Environment Not Activating**:
    
    -   Ensure you are using the correct command based on your OS.
    -   Verify that Python is installed and added to your system’s PATH.
2.  **Redis Connection Errors**:
    
    -   Make sure Redis is running on the correct port (`6379`  by default).
    -   Verify that your  `REDIS_URL`  in the  `.env`  file is correct.
3.  **Database Connection Errors**:
    
    -   Ensure PostgreSQL is running and accessible.
    -   Verify that your  `DATABASE_URL`  in the  `.env`  file is correct.
4.  **Celery Worker Issues**:
    
    -   Ensure Redis is running before starting the Celery worker.
    -   Double-check that your Celery tasks are properly registered and that the import paths are correct.
5.  **Missing Environment Variables**:
    
    -   Make sure all required environment variables are defined in the  `.env`  file.
    -   Run  `echo $VAR_NAME`  (replace  `$VAR_NAME`  with the environment variable name) in your terminal to check if it’s set.

By following this guide, you'll be well-equipped to develop, debug, and contribute to the project efficiently.
