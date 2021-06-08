# Dev_Hub
A task manager for users



The default username and password are `admin` and `123` 



Installing required python modules
`pip3 install -r req.txt`

For creating a new database type:
`python3 app.py initdb`

For running the server type:
`python3 app.py runserver`



Routes:
<h3>Public</h3>

`/signup` to create a new user 

`/login` if successful shows the token for editing the user entry 

`/update/<id>` accepts a POST request with an `x-access-token` header to edit or update entry info 

`/text` to insert a text after creating a user

`/create` creates a new entry without user registration 

`/home` shows all entries in the database 

<h3>Private </h3>

`admin` admin login page

`admin_edit/<id>` edit an entry as an admin
