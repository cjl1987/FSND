# Coffee Shop Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
export FLASK_APP=api.py;
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## Tasks

### Setup Auth0

1. DONE: Create a new Auth0 Account
2. DONE: Select a unique tenant domain
3. DONE: Create a new, single page web application
4. DONE: Create a new API
    - in API Settings:
        - Enable RBAC
        - Enable Add Permissions in the Access Token
5. DONE: Create new API permissions:
    - `get:drinks-detail`
    - `post:drinks`
    - `patch:drinks`
    - `delete:drinks`
6. DONE: Create new roles for:
    - Barista
        - can `get:drinks-detail`
    - Manager
        - can perform all actions
7. Test your endpoints with [Postman](https://getpostman.com). 
    - DONE Register 2 users - assign the Barista role to one and Manager role to the other.
    - DONE Sign into each account and make note of the JWT.
    - DONE Import the postman collection `./starter_code/backend/udacity-fsnd-udaspicelatte.postman_collection.json`
    - DONE Right-clicking the collection folder for barista and manager, navigate to the authorization tab, and including the JWT in the token field (you should have noted these JWTs).
    - DONE Run the collection and correct any errors.
    - TODO: Export the collection overwriting the one we've included so that we have your proper JWTs during review!

## Request for Token
https://cjl.eu.auth0.com/authorize?audience=CoffeeShop&response_type=token&client_id=Ui2Fz5kX2iuPo66jPRmkGmmscYQhTRWR&redirect_uri=https://localhost:8080/login-results


## Token Manager: (Permissions: "delete:drinks", "get:drinks-detail", "patch:drinks", "post:drinks") 
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJscHVVQXd6WllDOS1wZFRzaVVwWCJ9.eyJpc3MiOiJodHRwczovL2NqbC5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVkZDZiNjhmODdhMmEwMDE5OWI4ZWZhIiwiYXVkIjoiQ29mZmVlU2hvcCIsImlhdCI6MTU5MjE0NDc3NSwiZXhwIjoxNTkyMjMxMTc1LCJhenAiOiJVaTJGejVrWDJpdVBvNjZqUFJta0dtbXNjWVFoVFJXUiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmRyaW5rcyIsImdldDpkcmlua3MtZGV0YWlsIiwicGF0Y2g6ZHJpbmtzIiwicG9zdDpkcmlua3MiXX0.EJdo-ijyaftYhnSWeRHHVA6iZ0N3A6XhdL9pggLNXlfsPWUHcujN_bXMYvauze8fKdP5CrW04ZXebqOXnp9ZSQVqF42AE_qdWnrhiAovXFWEP_TH7eqN9mmYB2VKXYuWNmZxl_1CsBsmhLTkvtMhPNjDrRpssKKMRlSXmv3rCFt0UQrcZKuMgXkV2zhgdq94RHTuLJXfPNCHjQ4cbe1tFBolaS_Gy_r3pNWqLCE97-_n3lI3O8zWYxydmKyBJzrJf8xfArKLPXyEtg4yiDU-6O406RBlJH8kkGUJ9iKYjjJNPOedhVrMvDr7KA39TOgX6fMQJB-E_SYCEWjSGH4NwQ


## Token Barista: (Permissions: "get:drinks-detail")
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJscHVVQXd6WllDOS1wZFRzaVVwWCJ9.eyJpc3MiOiJodHRwczovL2NqbC5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVkZDZiNjhmODdhMmEwMDE5OWI4ZWZhIiwiYXVkIjoiQ29mZmVlU2hvcCIsImlhdCI6MTU5MjE0NDk4NCwiZXhwIjoxNTkyMjMxMzg0LCJhenAiOiJVaTJGejVrWDJpdVBvNjZqUFJta0dtbXNjWVFoVFJXUiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmRyaW5rcy1kZXRhaWwiXX0.d3Y02YfRGOH7SXFik_gir1zZPIVI1vdzULxJMj-JF7ByslXMjCzfnX2laoafq99wOad69jhlcAZpRQYFuusCKLYPZtXRor-vMp8tCLbYyUDkGr3v9lUAQPspHmHji1trpQzZTgNvJ7GMzlRxrHP_21yHWNVBZb3QYUjpXLousBE9tsf3dXA5Guh74_fpqlGz7bIglvZ9ez_z9lcHTmA0xn3Vg2pvhsiMBR-LdkOU1FCvGaBR4DZzy7yNEc-gULI04enAf5jmaAqmW4_r6bks8wsAgGDnKlufjFwBfKlU1VPKDg0XmTFKOSVzP6Vu5K1gyYCtGvOCePyrAWqf1kC4bQ

## Token Random: 
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJscHVVQXd6WllDOS1wZFRzaVVwWCJ9.eyJpc3MiOiJodHRwczovL2NqbC5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVkZDZiNjhmODdhMmEwMDE5OWI4ZWZhIiwiYXVkIjoiQ29mZmVlU2hvcCIsImlhdCI6MTU5MTkxMzkyOCwiZXhwIjoxNTkxOTIxMTI1LCJhenAiOiJVaTJGejVrWDJpdVBvNjZqUFJta0dtbXNjWVFoVFJXUiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOltdfQ.UmJCzrhrEfq0vR1KwOxEJ76Hqfb7ay2rzFHB7NKy3gnFqTns_uzTbYgPULOKPpmhEw9u29DOiNm2gvqMLmtajQaqToRuseN5rxiVGAZVbmSftXzQ4YMbbgWt0YHY-yG-DmdXsJUpjd0jRZrsqWyzLSMeovblsHGvMvcNvyLIRqjBShRehYXbA-wagVAeX3260rsusWJ-EPYvl3rg1dFNpw7lIdZ6t5xBhpaXYYR1K_Yq7J0i-nK9v8rIzmei_xS89ASiNpOPN60O_y1JV56rjkEBMyXQmbX-n8WUh6M0OChQYsnk3fo6rs-CX3VEmINTQTqHxYF2LW1mQkhHqixTzQ


### Implement The Server

There are `@TODO` comments throughout the `./backend/src`. We recommend tackling the files in order and from top to bottom:

1. `./src/auth/auth.py`
2. `./src/api.py`




