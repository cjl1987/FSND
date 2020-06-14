import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
db_drop_and_create_all()

## ROUTES
'''
@DONE - TODO implement endpoint
    DONE - GET /drinks
        DONE - it should be a public endpoint
        DONE - it should contain only the drink.short() data representation
    DONE - returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        DONE - or appropriate status code indicating reason for failure
'''


#GET endpoint to get drinks
@app.route('/drinks', methods=['GET'])
def get_drinks():
    try:
        drinks = []

        #get drinks from data base
        selection=Drink.query.all()
        
        #check whether selection is empty
        if len(selection) == 0:
            abort(422)
        
        #return all drinks in short() form
        for drinks_selected in selection:
            drinks.append(drinks_selected.short())
        
        return jsonify({
                        "success": True, 
                        "drinks": drinks
                        }), 200
    except: 
        abort(422)



'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        DONE - it should contain the drink.long() data representation
    DONE - returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        DONE - or appropriate status code indicating reason for failure
'''
#GET endpoint to get drinks-detail
@app.route('/drinks-detail', methods=['GET'])
def get_drinks_detail():
    try:
        drinks = []

        #get drinks from data base
        selection=Drink.query.all()
        
        #check whether selection is empty
        if len(selection) == 0:
            abort(422)
        
        #return all drinks in long() form
        for drinks_selected in selection:
            drinks.append(drinks_selected.long())
        
        return jsonify({
                        "success": True, 
                        "drinks": drinks
                        }), 200
    except: 
        abort(422)



'''
@TODO implement endpoint
    POST /drinks
        DONE - it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    DONE -returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        DONE - or appropriate status code indicating reason for failure
'''


# POST /drinks  
@app.route('/drinks', methods=['POST'])     
def create_drink():
    #get json object
    body = request.get_json()
    new_title = body.get('title', None)
    new_recipe = body.get('recipe', None)

    #cast new recipe to list
    if isinstance(new_recipe, dict):
        new_recipe = [new_recipe]   

    #check whether user input is complete
    if new_title == None:
        abort(422) 
    if new_recipe == None:
        abort(422) 

    try:
        #add row in data base
        drink = Drink()
        drink.title = new_title
        drink.recipe = json.dumps(new_recipe)
        drink.insert()

        #return json response          
        return jsonify({
                        "success": True,
                        "drinks": [drink.long()]
                        })
    except:
        abort(422)



'''
@TODO implement endpoint
    PATCH /drinks/<id>
        DONE - where <id> is the existing model id
        TODO - it should respond with a 404 error if <id> is not found
        DONE - it should update the corresponding row for <id>
        TODO - it should require the 'patch:drinks' permission
        DONE - it should contain the drink.long() data representation
    DONE - returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        DONE - or appropriate status code indicating reason for failure
'''

#PATCH drink by provided drink_id
@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
def drinks_update(drink_id):
    #load PATCH body
    body = request.get_json()

    #get drink by id
    try:
        drink = Drink.query.filter(Drink.id==drink_id).one_or_none()
       
        #error 404
        if drink is None:
            abort(404)

        #prepare body
        if body.get('title'):
            drink.title = body.get('title')
        if body.get('recipe'):
            drink.recipe = json.dumps(body.get('recipe'))
        
        #update data base
        drink.update()
        return jsonify({
                        "success": True, 
                        "drinks": drink.long()
                        }), 200
    except:
        abort(422)



'''
@TODO implement endpoint
    DELETE /drinks/<id>
        DONE - where <id> is the existing model id
        TODO -  it should respond with a 404 error if <id> is not found
        DONE - it should delete the corresponding row for <id>
        TODO - it should require the 'delete:drinks' permission
    DONE - returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        DONE - or appropriate status code indicating reason for failure
'''

#Delete drink
@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
def delete_drink(drink_id):
    
    try: 
        #get drink by drink_id
        drink = Drink.query.filter(Drink.id==drink_id).one_or_none() 

        #error 404
        if drink is None:
            abort(404)

        #delete row in data base
        drink.delete()
   
        return jsonify({
                        'success' : True, 
                        'delete': drink_id
                        }), 200

    except: 
        abort(422)



## Error Handling

#Error-Handler 422
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 422,
                    "message": "unprocessable"
                    }), 422


#Error-Handler 404
@app.errorhandler(404)
def resource_not_found(error):
    return jsonify({
                    "success": False,
                    "error": 404, 
                    "message": "resource not found"
                    }), 404


#Error-Handler 400
@app.errorhandler(400)
def bad_request(error):
    return jsonify({
                    "success": False, 
                    "error": 400,
                    "message": "bad request"
                    }), 400

'''
@TODO implement error handler for AuthError
    error handler should conform to general task above 
'''

