Clone Project
============
This project is a medical records management system built using Django

```
git clone https://github.com/Prosoffice/medi2dataInterviewTest.git
```

Installation
============
You can create a virtual environment as follows:

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Set up DB
=========

The following commands create the required database tables in a
local sqlite db

```
# run migrations
cd medi2data
./manage.py migrate
````

Run test suite
==============

```
./manage.py test
````
Create an HealthCare Admin account
============
```
 ./manage.py createsuperuser
```
Follow the prompt in creating an admin account using a username, email and password

Run project
===========

```
./manage.py runserver
````

This runs the Django devserver on port 8000.

Go to http://localhost:8000/admin on your browser and authenticate using the admin credentials created earlier
