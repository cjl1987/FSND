#Full Stack Trivia API:

This trivia game enables you to compete and challenge yourself with your colleagues and friends. The project provides an API and test suite with the following possibilities:

1) Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer. 
2) Delete questions.
3) Add questions and require that they include question and answer text.
4) Search for questions based on a text query string.
5) Play the quiz game, randomizing either all questions or within a specific category. 


##Getting Started

Pre-requisites and Local Development

Developers using this project should already have Python3, pip and node installed on their local machines.

###Setup Frontend
This project depends on Nodejs and Node Package Manager (NPM). Before continuing, you must download and install Node (the download includes NPM) from [https://nodejs.com/en/download](https://nodejs.org/en/download/).

This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. After cloning, open your terminal and run:

```bash
npm install
```

### Running your Frontend in Dev Mode

The frontend app was built using create-react-app. In order to run the app in development mode use ```npm start```. You can change the script in the ```package.json``` file. 

Open [http://localhost:3000](http://localhost:3000) to view it in the browser. The page will reload if you make edits.<br>

```bash
npm start
```

###Setup Backend 

First have your virtual environment setup and running in `/starter`
	
```bash
source env/bin/activate 
```

Then install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.


###Running Backend server in Dev Mode

From within the `/backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 


### Testing
To run the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

>
##API Reference

###Getting started 


##Authors and API Reference
Christoph Leichte edited and created the API interface (__init__.py), test suite (test_flaskr.py) and README. The other files in this project were provided by Udacity in the framework of the Nanodegree 'Full Stack Web Developer'.


##Acknowledgements
Great thanks to Nikolai, pushing my progress.


