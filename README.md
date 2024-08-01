# MCIT Alumni Search Slack Bot

## Set Up

Before running your code, ensure you are in the virtual environment by activating it. The virtual environment isolates dependencies needed for the project, ensuring consistency and avoiding conflicts with system-wide packages or other projects. Once activated, you don't need to worry about installing dependencies globally.

### Activate the Virtual Environment

Each time you work on the project, activate the virtual environment:
```bash
# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

**Installing New Packages**
When you need to install new packages, make sure the virtual environment is activated:
```bash
pip install <package-name>
```
**Updating requirements.txt**
After installing new packages, update the requirements.txt file to ensure all dependencies are listed:
```bash
pip freeze > requirements.txt
```

Others can then install these dependencies using:
```bash
pip install -r requirements.txt
```