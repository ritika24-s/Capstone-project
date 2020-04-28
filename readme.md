Motivation
A basic casting agency app to fulfill my learning from FSND.

Project Dependencies
### Python 3.7.4
Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/windows.html?highlight=installing%20latest%20version%20python)

### PIP Dependencies
pip install -r requirements.txt
This will install all of the required packages for this project.

### Running the server
From within the root directory, each time you open a new terminal session, run:

export FLASK_APP=app.py
To run the server, execute:

flask run --reload
The --reload flag will detect file changes and restart the server automatically.

Tasks
### Setup Auth0
Create a new Auth0 Account
Select a unique tenant domain
Create a new, single page web application
Create a new API - in API Settings:
Enable RBAC
Enable Add Permissions in the Access Token
Create new API permissions:
get:actors
get:movies
post:actor
post:movie
patch:actor
patch:movie
delete:actor
delete:movie
Create new roles for:
Casting Assistant
- can get:actors and get: movies
Casting Director
- can perform all actions of Casting Assistant
- can post:actor and delete:actor
- can patch:actor and patch:movie
Executive Producer
- can perform all actions
Register 3 users
Assign the Casting Assistant role to one
Assign the Casting Director role to another
Assign the Executive Producer role to the last
Sign into each account and make note of the JWT.(https://fsndca.auth0.com/authorize?audience=casting agency&response_type=token&client_id=YAZXgqjhCCOCw5EIg4xlQeXukeNKkBmr&redirect_uri=http://localhost:8100)
Test the endpoints with the latest version of [Postman](https://getpostman.com).
Import the postman collection "./udacity-fsnd-castingagency.postman_collection.json"
Right-clicking the collection folder for Casting Assistant, Casting Director and Executive Producer, navigate to the authorization tab, and include the JWT in the token field (you should have noted these JWTs).
Run the collection.
The collection points to live application: https://abgarg-capstone.herokuapp.com//
### Testing
To run the unit tests, execute:
python test_app.py
Note - make sure the 3 header variables are updated for each role JWT collected.

API behavior and RBAC controls
### Endpoints
GET /actors
GET /movies
PATCH /actors/<id>
PATCH /movies/<id>
POST /actors
POST /movies
DELETE /actors/<id>
DELETE /movies/<id>
GET /actors
Returns a list of all actors
Requires auth permission get:actors
Request: None
Response:
{
"actors": [
    {
        "age": 35,
        "gender": "Female",
        "id": 1,
        "name": "Scarlett Johansson"
    },
    {
        "age": 38,
        "gender": "Male",
        "id": 2,
        "name": "Chris Evans"
    }
],
"success": true
}
GET /movies
Returns a list of all movies
Requires auth permission get:movies
Request: None
Response:
{
"movies": [
    {
        "id": 1,
        "release_date": "2019",
        "title": "Avengers: Endgame"
    },
    {
        "id": 2,
        "release_date": "2020",
        "name": "Black Widow"
    }
],
"success": true
}
PATCH /actors/<id>
Updates a selected actor by id
Requires auth permission patch:actor
Request:
{
    "name": "Updated Name",
    "age": 50,
    "gender": "Male"
}
Response:
{
    "success": true,
    'actors': [ {
    "name": "Updated Name",
    "age": 50,
    "gender": "Male"
}]
}
PATCH /movies/<id>
Updates a selected movie by id
Requires auth permission patch:movie
Request:
{
    "title": "Updated Title",
    "release_date": "2018"
}
Response:
{
    "success": true,
    "movies":[{
    "title": "Updated Title",
    "release_date": "2018"
}]
}
POST /actors
Adds a new actor
Requires auth permission post:actor
Request:
{
    "name": "Robert Downey Jr.",
    "age": 54,
    "gender": "Male"
}
Response:
{
    "id": 3,
    "success": true
}
POST /movies
Adds a new movie
Requires auth permission post:movie
Request:
{
    "title": "The Hunt",
    "release_date": "2020"
}
Response:
{
    "id": 3,
    "success": true
}
DELETE /actors/<id>
Deletes an actor by id
Requires auth permission delete:actor
Request: None
Response:
{
    "success": true
}
DELETE /movies/<id>
Deletes a movie by id
Requires auth permission delete:movie
Request: None
Response:
{
    "success": true
}