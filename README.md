- ### Install the requirements:

```
pip install -r requirements.txt
```

- ### Configure MySQL database

- ### Set the following environment variables:

```
MYSQL_USER=<your_mysql_user>
MYSQL_PASSWORD=<your_mysql_user_password>
MYSQL_SERVER=<your_mysql_server>
MYSQL_DATABASE=<your_mysql_database_name>
```

- ### Run web app

```
python -m flask run
```

or

```
gunicorn -w 4 app:app
```
