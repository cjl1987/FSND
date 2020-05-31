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
	- Base URL: This application is only run locally. Therefore the host is http://127.0.0.1:5000/ 
	- Authentication: This version does not require authentication or API keys.

###Endpoints

###Error Handling
The error response is in JSON in the following format:
	{
	     	'success':False, 
	      	'error': 400, 
	      	'message':'Bad request'
	}

The API handles the following types of errors:
	- 400: 	'Bad request' 
	- 404:	'Not found' 
	- 422:	'Unprocessable Entity'


####GET /categories
- General	
	- Returns all available categories
- Sample
	- curl http://127.0.0.1:5000/categories
	
	{
	  "categories": {
	    "1": "Science", 
	    "2": "Art", 
	    "3": "Geography", 
	    "4": "History", 
	    "5": "Entertainment", 
	    "6": "Sports"
	  }, 
	  "success": true
	}

####GET /questions
- General	
	- Returns a list of question objects, success value, categories and total number of questions.
	- Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.
- Sample
	- curl http://127.0.0.1:5000/questions
	{
	  "categories": {
	    "1": "Science", 
	    "2": "Art", 
	    "3": "Geography", 
	    "4": "History", 
	    "5": "Entertainment", 
	    "6": "Sports"
	  }, 
	  "questions": [
	    {
	      "answer": "Maya Angelou", 
	      "category": 4, 
	      "difficulty": 2, 
	      "id": 5, 
	      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
	    }, 
	    {
	      "answer": "Edward Scissorhands", 
	      "category": 5, 
	      "difficulty": 3, 
	      "id": 6, 
	      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
	    }, 
	    {
	      "answer": "Brazil", 
	      "category": 6, 
	      "difficulty": 3, 
	      "id": 10, 
	      "question": "Which is the only team to play in every soccer World Cup tournament?"
	    }, 
	    {
	      "answer": "Uruguay", 
	      "category": 6, 
	      "difficulty": 4, 
	      "id": 11, 
	      "question": "Which country won the first ever soccer World Cup in 1930?"
	    }, 
	    {
	      "answer": "The Palace of Versailles", 
	      "category": 3, 
	      "difficulty": 3, 
	      "id": 14, 
	      "question": "In which royal palace would you find the Hall of Mirrors?"
	    }, 
	    {
	      "answer": "Agra", 
	      "category": 3, 
	      "difficulty": 2, 
	      "id": 15, 
	      "question": "The Taj Mahal is located in which Indian city?"
	    }, 
	    {
	      "answer": "Escher", 
	      "category": 2, 
	      "difficulty": 1, 
	      "id": 16, 
	      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
	    }, 
	    {
	      "answer": "Mona Lisa", 
	      "category": 2, 
	      "difficulty": 3, 
	      "id": 17, 
	      "question": "La Giaconda is better known as what?"
	    }, 
	    {
	      "answer": "One", 
	      "category": 2, 
	      "difficulty": 4, 
	      "id": 18, 
	      "question": "How many paintings did Van Gogh sell in his lifetime?"
	    }, 
	    {
	      "answer": "Jackson Pollock", 
	      "category": 2, 
	      "difficulty": 2, 
	      "id": 19, 
	      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
	    }
	  ], 
	  "success": true, 
	  "total_questions": 14
	}


####DELETE /questions/<int:id>
- General	
	- Deletes one question by id using url parameter
	- Returns the id of deleted question
- Sample
	- curl -X DELETE http://127.0.0.1:5000/questions/6

	{
	  "deleted_question": 6, 
	  "success": true
	}

####POST /questions
This enpoints allows two possibilities:

1) Create a new question: If no search term is included as JSON: 
- General: 
	- One new question is created and added to the database based on the JSON parameters.
	- Returns a JSON object including the created question and paginated questions
- Sample
	- curl -X POST -H "Content-Type: application/json" -d '{"question":"How high is the Eiffel tower?", "answer":"300 meter", "difficulty": 4, "category":"1"}' http://127.0.0.1:5000/questions
	{
		
	====================HIER RESPONSE BODY VON CREATE QUESTION einfügen========

	}

2) Return a search result from question
- General: 
	- Searches through all questions based on the JSON search term
	- Returns a JSON object including paginated questions, total number of questions, success and categories.
- Sample
	- curl -X POST -H "Content-Type: application/json" -d '{"searchTerm":"paint"}' http://127.0.0.1:5000/questions

	{
	  "categories": {
	    "1": "Science", 
	    "2": "Art", 
	    "3": "Geography", 
	    "4": "History", 
	    "5": "Entertainment", 
	    "6": "Sports"
	  }, 
	  "questions": [
	    {
	      "answer": "One", 
	      "category": 2, 
	      "difficulty": 4, 
	      "id": 18, 
	      "question": "How many paintings did Van Gogh sell in his lifetime?"
	    }, 
	    {
	      "answer": "Jackson Pollock", 
	      "category": 2, 
	      "difficulty": 2, 
	      "id": 19, 
	      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
	    }
	  ], 
	  "success": true, 
	  "total_questions": 2
	}


####GET /categories/<int:id>/questions
- General: 
	- Gets questions from database by categors id provided in url parameter
	- Returns a JSON object with paginated questions, succes, categories and number of total questions
- Sample
	- curl http://127.0.0.1:5000/categories/4/questions
	{
	  "questions": [
	    {
	      "answer": "Maya Angelou", 
	      "category": 4, 
	      "difficulty": 2, 
	      "id": 5, 
	      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
	    }, 
	    {
	      "answer": "Scarab", 
	      "category": 4, 
	      "difficulty": 4, 
	      "id": 23, 
	      "question": "Which dung beetle was worshipped by the ancient Egyptians?"
	    }
	  ], 
	  "success": true, 
	  "total_questions": 2
	}


####POST /quizzes
- General: 
	- Starts trivia game based on a selected category or ALL categories
	- Expects a JSON object with category and previous question id's included
	- Returns a JSON object with random question from category, not included in previous questions and success
- Sample:
	- curl -X POST -H "Content-Type: application/json" -d '{"previous_questions":[20],"quiz_category":{"type":"Science","id":"1"}}' http://127.0.0.1:5000/quizzes
	{
	  "question": {
	    "answer": "Alexander Fleming", 
	    "category": 1, 
	    "difficulty": 3, 
	    "id": 21, 
	    "question": "Who discovered penicillin?"
	  }, 
	  "success": true
	}




##Authors and API Reference
Christoph Leichte edited and created the API interface (__init__.py), test suite (test_flaskr.py) and README. The other files in this project were provided by Udacity in the framework of the Nanodegree 'Full Stack Web Developer'.


##Acknowledgements
Great thanks to Nikolai, pushing my progress.


