import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

#Paginate questions 
def paginate_questions(request, selection):
  page = request.args.get('page', 1, type=int)
  formatted_questions = [question.format() for question in selection]
  start = (page-1)*QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE
  if len(formatted_questions) == 0:
    abort(404)
  return formatted_questions[start:end]


#List 'Categories' 
def formatted_categories_special():
  selection = Category.query.order_by(Category.id).all()
  formatted_categories={}
  for category in selection:
    formatted_categories[str(category.id)]=category.type
  
  if  len(formatted_categories)==0:
    abort(404)  
  return formatted_categories



def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
 
  #Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  CORS(app, resources={'/': {'origins': '*'}})
 
 
  #Use the after_request decorator to set Access-Control-Allow 
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, DELETE')
    return response
 
  # Get Categories
  @app.route('/categories', methods=['GET'])
  def retrieve_categories():  
   
    return jsonify({
      'success':True,
      'categories': formatted_categories_special()
      })


  # GET endpoint to handle requests for questions
  @app.route('/questions', methods=['GET'])
  def retrieve_questions():
    selection = Question.query.order_by(Question.id).all()
    
    return jsonify({
      'success' : True,
      'questions': paginate_questions(request, selection),
      'total_questions' : len(selection),
      'categories' : formatted_categories_special()
    })


  #Delete endpoint to delete single questions
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    
    try: 
      question = Question.query.filter(Question.id == question_id).one_or_none() 

      if question is None:
        abort(404)

      question.delete()
    
      return jsonify({
        'success' : True, 
        'deleted_question': question_id
      })
    
    except: 
      abort(422)

  
  # POST endpoint to create new questions AND to get questions based on a search term.  
  @app.route('/questions', methods=['POST'])     
  def create_question():
    body = request.get_json()
    
    if body.get('searchTerm') is not None:
      try:
        selection = Question.query.filter(Question.question.ilike('%'+body.get('searchTerm')+'%')).all()
        return jsonify({
          'success' : True,
          'questions': paginate_questions(request, selection),
          'total_questions' : len(selection),
          'categories' : formatted_categories_special(),

        })

      except:
        abort(422)
    
    else:   
      new_question = body.get('question', None) 
      new_answer = body.get('answer', None)
      new_category = body.get('category', None)
      new_difficulty = int(body.get('difficulty', None))
      print("in create_question gesprungen")
      print(new_question)
      print(type(new_question))
      print(new_answer)
      print(type(new_answer))
      print(new_category)
      print(type(new_category))
      print(new_difficulty)
      print(type(new_difficulty))
      
      try:
        question = Question(question=new_question, answer=new_answer, category=new_category, difficulty=new_difficulty)
        print(question.answer)
        print('Difficulty: Value & Type: ')
        print(question.difficulty)
        print(type(question.difficulty))
        question.insert()              
           
        
        return jsonify({
          'success': True
        })
      except: 
        abort(422)
    
 
  #GET endpoint to get questions based on category.
  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def get_questions_by_category(category_id):
    selection=Question.query.filter(Question.category==category_id).all()
    
    return jsonify({
      'succes':True,
      'questions': paginate_questions(request, selection),
      'total_questions' : len(selection),     
    })


  #POST endpoint to get questions to play the quiz
  @app.route('/quizzes', methods=['POST'])
  def play_trivia():
    body=request.get_json()
    to_be_removed=[]

    #check whether category 'ALL' is selected
    if body.get('quiz_category').get('id') == 0:
      selection = Question.query.all()
    else:
      selection = Question.query.filter(Question.category==body.get('quiz_category').get('id')).all()

    #filter if a question was already shown in current game
    for question in selection:
      for previous_question_id in body.get('previous_questions'):        
        if question.id == previous_question_id:
          to_be_removed.append(question)  
    
    #remove the already shown questions from selection
    for question_to_remove in to_be_removed:
      selection.remove(question_to_remove)
    

    #check if there is a remaining question
    if len(selection) ==0 :
      return jsonify({
        'success' : True,                       
      })
    #if question remains, randomize and return one question
    else:
      x=random.randint(0,(len(selection)-1))
      return jsonify({
        'success' : True,
        'question': selection[x].format()                         
        })


  #Error-Handler 400
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      'success':False, 
      'error': 400, 
      'message':'Bad request'
    }), 400
  
  #Error-Handler 422
  @app.errorhandler(422)
  def unprocessable_entity(error):
    return jsonify({
      'success': False, 
      'error' : 422,
      'message': 'Unprocessable Entity'
    }), 422

  #Error-Handler 404
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
        'success': False, 
        'error': 404,
        'message': 'Not found'    
        }), 404
  
  
  return app
