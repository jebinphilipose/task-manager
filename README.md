# Task Manager

## Project Overview

To make REST API endpoints to trigger long running tasks with ability to pause, resume and stop the tasks.

## Getting Started

### Prerequisites

* Git
* Docker
* Docker Compose

### Project Setup

1. Clone this repo: `git clone https://github.com/jebinphilipose/task-manager.git && cd task-manager`
2. Create a `.env` file in project root and set **SECRET_KEY**, **ALLOWED_HOSTS**, **DEBUG**, **DB_NAME**, **DB_USER**, **DB_PASSWORD**, **DB_HOST**, **DB_PORT**, **CELERY_BROKER_URL**, **CELERY_RESULT_BACKEND**
3. Run the server: `docker-compose up --build`
4. (Optional) Open a new terminal shell and run this to load initial DB data:
    
    ```
    $ docker-compose exec django sh
    $ python manage.py loaddata mydata.json
    ```
    
    Don't run this if you want to test upload csv flow first, this data will be useful if you want to test download csv flow.

5. Make requests


## API Endpoints

* POST `/api/v1/upload/` --> Creates a new task for CSV upload. Input: `users.csv`
  
  ```
  curl --location --request POST 'http://localhost:8000/api/v1/upload/'
  ```

* POST `/api/v1/download/` --> Creates a new task for CSV download. Output: `export.csv`
  
  ```
  curl --location --request POST 'http://localhost:8000/api/v1/download/' \
  --header 'Content-Type: application/json' \
  --data-raw '{
      "from_date": "1900-01-31 19:51:44"
  }'
  ```

* PATCH `/api/v1/task/1/pause/` --> Pauses a task
  
  ```
  curl --location --request PATCH 'http://localhost:8000/api/v1/task/1/pause/'
  ```

* PATCH `/api/v1/task/1/resume/` --> Resumes a task
  
  ```
  curl --location --request PATCH 'http://localhost:8000/api/v1/task/1/resume/'
  ```

* PATCH `/api/v1/task/1/cancel/` --> Cancels a task
  
  ```
  curl --location --request PATCH 'http://localhost:8000/api/v1/task/1/cancel/'
  ```

## How to Test

* Create a new upload task
* While it's processing, hit the pause API endpoint to pause the task
* Login to psql shell: `docker-compose exec db psql --username=<db_user> --dbname=<db_name>`
* Check the no. of records: `select count(*) from api_user;`
* Now resume the task by hitting the endpoint
* Again pause
* Now check no. of records again, the count will be increased
* If you let it complete, the entire CSV will be imported to DB
* If you cancel the task, all changes will be undone, you can verify it through psql console