# Fake CSV generator

An online service for generating CSV files with fake (dummy) data using Python and Django


#### Usage

- User can create any number of data schemas to create datasets with fake data.
- Each such data schema has a name and the list of columns with names and specified data types.
- Users can build the data schema with any number of columns.
- After creating the schema the user can input the number of records he/she needs to generate.
- After generating process the result is saved in the file and user can download datasets.


The application has been deployed to pythonanywhere http://dmytropodolynnyi.pythonanywhere.com/

For testing app use login ``username`` and password ``userpassword``


#### Instalation

● Create a python virtual environment and install dependencies from requirements.txt
Execute in terminal:
````
python3 -m venv venv
````
If you are using Windows, then :

````
venv\Scripts\activate
````
If UNIX/LINUX, then :
````
source venv\bin\activate
````

Install requirements for project
````
pip install -r requirements.txt
````

● Migrate the database 
````
python manage.py makemigrations
````
````
python manage.py migrate
````

●  Run the server 
````
python manage.py runserver
````

●  Done. Use the App