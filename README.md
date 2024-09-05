# FastAPI Assignment
author: hieu.nguyenchi5@nashtechglobal.com

- A FastAPI application to learn how to use FastAPI – Uvicorn – SQL Alchemy – Alembic.
- Using PostgreSQL for DB Storage
- Apply: Validation, Model, Query, Routing, Authorizer


# How to Setup
<b>I used Python 3.12.5 in local for this assignment</b>

- Create a virtual environment using `virtualenv` module in python.
```bash
# Install module (globally)
pip install virtualenv

# Generate virtual environment
virtualenv --python=<your-python-runtime-version> venv

# Activate virtual environment
source venv/bin/activate

# Install depdendency packages
pip install -r requirements.txt
```
- Configure `.env` file by creating a copy from `.env.sample`
- Setup a postgres docker container
```bash
docker run -p 5432:5432 --name postgres -e POSTGRES_PASSWORD=<your-preferred-one> -d postgres:14
```
- At `app` directory, run `alembic` migration command. Please make sure your postgres DB is ready and accessible. In case you want to use `SQLite` instead, please be sure to configure the `env.py` file in `alembic` folder to support `batch execution` since `SQLite` does not support `ALTER` command, which is needed to configure the foreign key and establish the indexes.
```bash
# Migrate to latest revison
alembic upgrade head

# Dowgragde to specific revision
alembic downgrade <revision_number>

# Downgrade to base (revert all revisions)
alembic downgrade base

# Create new revision
alembic revision -m <comment>
```
- Run `uvicorn` web server from `app` directory (`reload` mode is for development purposes)
```bash
uvicorn main:app --reload
```

Open http://localhost:8000/docs to check All API

# Note
## 1. Company
- I inserted 1 record for company with id = 1.

## 2. User
- I inserted 2 records for user (1 for admin, 1 for user) with the same password. 
- You can change password via .env file with "DEFAULT_PASSWORD" field.
- The password using <b>HS256</b> to hash.
- The user details need to login to get current user information.

## 3. Task
- Only <b>Admin</b> can create new task
- When the Admin creates or update a task, if they don't input "user_id", the task will be for the admin (task.user_id = admin.id)
- When the User update a task, they only can update for themselves. The Admin can update for everyone.
