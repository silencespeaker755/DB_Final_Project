# DB_Final_Project

## ORM Model

### Installation
It needs several packages to run the code:
* pycryptodome
* python-dotenv

Alternatively, you can install them directly the `requirements.txt`.
```bash
pip install -r requirements.txt
```

### Demo
Run the following command in the terminal:
```bash
python3 main.py examples.csv
```

#### Options
```
usage: main.py [-h] [-d DB_NAME] info

positional arguments:
  info                  load user's info & key

optional arguments:
  -h, --help            show this help message and exit
  -d DB_NAME, --db_name DB_NAME
                        choose current database. default: test
```

The script will load records from `examples.csv` into the database `test`, and encrypt the specific columns.

## SQLite3 User Extension

To compile the user-defined modules:
```bash
cc --shared -fPIC -I sqlite-autoconf-3350500 crypto-functions.c -o crypto-functions.so
```
Replace ```sqlite-autoconf-3350500``` with proper sqlite3 installed directory


Example use case in sqlite3 CLI:

```
sqlite>.load crypto-functions.so

sqlite>INSERT INTO <table name> VALUES (Encrypt_Caesar(<insert value>), ...)
```
