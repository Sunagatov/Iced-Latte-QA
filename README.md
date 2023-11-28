# Online-Store-QA
Automated tests in Python for project Online-Store -> https://github.com/Sunagatov/Online-Store/

## Instruction
For running tests should be created configs.py in root directory of format:
```Python
HOST = '<URL:port to app Online-Store>'
HOST_DB = '<URL to database of service>'
PORT_DB = '<port to database of service>'
DB_NAME = '<name database>'
DB_USER = '<username for connect to database>'
DB_PASS = '<password for connect to database>'
DEFAULT_PASSWORD = '<default password for test users>'
JWT_SECRET = '<default secret for JWT>'
```

## Report
(!) BE SURE TO INSTALL ALLURE -> https://allurereport.org/docs/gettingstarted/installation/

To get the Allure report on the local computer, follow these steps in root directory:
```bash
python -m pytest ./tests --alluredir=allure_report --clean-alluredir
allure serve allure_report
```

## Pre-commit hooks
For running pre-commit hooks should be installed pre-commit -> https://pre-commit.com/#install
```bash
pre-commit install
```
