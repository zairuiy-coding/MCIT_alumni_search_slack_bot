# 🎓 MCIT Alumni Search Slack Bot

## 📝 Overview

The MCIT Alumni Search Slack Bot is a robust tool designed to help MCIT students easily search for and retrieve information about alumni from the MCIT program via Slack commands. Leveraging the power of the Slack API for seamless integration, OpenAI for sophisticated natural language processing, and PostgreSQL for reliable data storage, this bot ensures efficient and concurrent handling of user queries. Additionally, it utilizes Redis for session management to provide a smooth and consistent user experience, preventing duplicate messages and managing tasks asynchronously with Celery.
## ✨ Key Features

-   **Slack Integration**: Seamlessly interacts with users in Slack through commands and message events.
-   **Natural Language Processing**: Uses OpenAI's API to process and understand user queries.
-   **Database Management**: Stores and retrieves alumni data from a PostgreSQL database.
-   **Asynchronous Task Processing**: Uses Celery and Redis to handle background tasks efficiently.
-   **Session Management**: Utilizes Redis for session management to ensure a smooth user experience.

## 🗂️ Project Structure

-   **`app.py`**: The main entry point for the Flask application.
-   **`bot/`**: Contains the core bot logic, including command handlers, event processors, and utility functions.
-   **`db/`**: Manages database connections and queries.
-   **`config.py`**: Handles configuration, including environment variables.
-   **`DEVELOPMENT.md`**: A detailed guide for setting up the development environment and workflow.
-   **`README.md`**: Provides an overview of the project and general instructions.

## 🏗️ Architecture Overview

Below is a UML class diagram that provides an overview of the main components of the system and their interactions.

![UML_MCIT_Slack_Bot](UML_MCIT_Slack_Bot.png)

## ⚙️ Setup and Installation

For detailed setup and installation instructions, including how to configure your environment, install dependencies, and run the application, please refer to the  [DEVELOPMENT.md](DEVELOPMENT.md).