# dd2477-project

DD2477 Search Engines &amp; Information Retrieval Systems project (Group 10)

## Setup Instructions

### Elasticsearch

You can set elastic search enviromemnt following instruction at [elasticsearch-tutorial.md](elasticsearch-tutorial.md).
It uses docker, so before set the environment of Elasticsearch, please make sure you already install dokcer.

### Required Environment
- Python: 3.10

### Required Packages

1. Install `virtualenv`, either via the OS's package manager or `pip install virtualenv`.
2. Create a virtual environment: `virtualenv venv`.
3. Activate the virtual environment: `source venv/bin/activate`.
4. Install the required packages: `pip install -r requirements.txt`.

## Running things

First things first, to create or recreate the SQLite database, run the `sqlitedb.py` script:

```bash
python -m utils.sqlitedb
```

Choose option '1' to create the database for the first time, or option '2' to delete and to recreate it.

### Terminal Interface

Run, at the root of the project:

```bash
python -m terminal.tui
```

### Django Server

```bash
# Apply migrations
python manage.py migrate
# Run the server
python manage.py runserver
```
