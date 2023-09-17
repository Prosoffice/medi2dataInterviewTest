Installation
============

This project is a medical records management system built using Django

You can create a virtual environment as follows:

```
cd medi2data
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Set up DB
=========

The following commands create the required database tables in a
local sqlite db, and load in some sample data.

```
source venv/bin/activate
cd medi2data
# run migrations
./manage.py migrate
````

Run project
===========

```
source venv/bin/activate
cd medi2data
./manage.py runserver
````

This runs the Django devserver on port 8000.

You can now access the API using curl, e.g.

```
curl http://localhost:8000/admin
```

or go to http://localhost:8000/admin in your browser


Run test suite
==============

```
source venv/bin/activate
cd medi2data
./manage.py test
````