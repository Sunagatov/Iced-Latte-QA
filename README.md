# Iced Latte QA
Automated tests in Python for project Iced Latte -> https://github.com/Sunagatov/Iced-Latte/

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
## Start Local Iced-Latte Backend

```sh
./start_be.sh [<commit_hash>]
```

> Notes: 
> * optional `commit_hash` is a hash of a commit from `development` branch, default is the latest
> * it might be necessary to make script executable before the first run `chmod +x ./start_be.sh`
> * the script will pull the specified version of BE image and start BE, Postgres and Minio
> * periodically clean up the system by running [`docker rm`](https://docs.docker.com/engine/reference/commandline/container_rm/)

Swagger will be available here [http://localhost:8083/api/docs/swagger-ui/index.html](http://localhost:8083/api/docs/swagger-ui/index.html).

To check the logs use:

```sh
docker-compose -f docker-compose.local.yml logs --tail 500
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
