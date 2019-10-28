from flask import request, jsonify, make_response,  Blueprint
import uuid
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from authentication import token_required
from models import *
import datetime
import os
import psycopg2 



api_request= Blueprint('all', __name__)   #create a api_request blueprint

   

@api_request.route('/user', methods=['GET'])
@token_required
def get_all_users(current_user):

    if not current_user.admin:
        return jsonify({"message": "Cannot perform that operation!"})
    users = User.query.all()

    output = []

    for user in users:
        user_data = {}   #new dict created from the database
        user_data['public_id']= user.public_id 
        user_data['name']= user.name
        user_data['password']= user.password
        user_data['admin']= user.admin

        output.append(user_data)

    return jsonify({'users': output})

@api_request.route('/user/<public_id>', methods=['GET'])
@token_required
def get_one_user(current_user,public_id):

    if not current_user.admin:
        return jsonify({"message": "Cannot perform that operation!"})

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
         return jsonify({'message': 'No user found'})
    
    user_data = {}   #new dict created from the database
    user_data['public_id']= user.public_id 
    user_data['name']= user.name
    user_data['password']= user.password
    user_data['admin']= user.admin

    return jsonify({"user": user_data })

@api_request.route('/user', methods=['POST'])
@token_required
def create_user():

    if not current_user.admin:
       return jsonify({"message": "Cannot perform that operation!"})

    data = request.get_json()   #passes json data to the variable and saves as data variable

    hashed_password = generate_password_hash(data['password'], method='sha256') #hashed password

    new_user = User(public_id=str(uuid.uuid4()), name=data['name'], password= hashed_password, admin= False)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message':'New User created'})

@api_request.route('/user/<public_id>', methods=['PUT'])
@token_required
def promote_user(current_user,public_id):

    if not current_user.admin:
        return jsonify({"message": "Cannot perform that operation!"})

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
         return jsonify({'message': 'No user found'})

    user.admin = True
    db.session.commit()
    return jsonify({'message':'The user has been promoted'})

@api_request.route('/user/<public_id>', methods=['DELETE'])
@token_required
def delete_user(current_user,public_id):

    if not current_user.admin:
        return jsonify({"message": "Cannot perform that operation!"})    
    
    user = User.query.filter_by(public_id=public_id).first()

    if not user:
         return jsonify({'message': 'No user found'})

    db.session.delete(user)
    db.session.commit() 

    return jsonify({'message':"The user has been deleted!"}) 

@api_request.route('/login', methods=['GET', 'POST'])
def login(): 
    auth = request.authorization  

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required"'})

    user = User.query.filter_by(name=auth.username).first()

    if not user:
        return make_response('Could not verify', 401, {' WWW-Authenticate': 'Basic realm="Login required"'})

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'public_id': user.public_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, os.getenv('SECRET_KEY'))    
        
        return jsonify({'token': token.decode('UTF-8')})

    return make_response('Could not verify', 401, {' WWW-Authenticate': 'Basic realm="Login required"'})   

@api_request.route('/todo', methods=['GET'])
@token_required
def get_all_todos(current_user):

    todos = Todo.query.filter_by(user_id= current_user.id).all()

    output= []

    for todo in todos:
        todo_data = {}
        todo_data['id'] = todo.id
        todo_data['text'] = todo.text
        todo_data['complete'] = todo.complete

        output.append(todo_data)

    return jsonify({"todos": output})

@api_request.route('/todo/<todo_id>', methods=['GET'])
@token_required
def get_one_todo(current_user, todo_id):

    todo = Todo.query.filter_by(id=todo_id, user_id = current_user.id).first()

    todo_data = {}
    todo_data['id'] = todo.id
    todo_data['text'] = todo.text
    todo_data['complete'] = todo.complete

    return jsonify({todo_data})

@api_request.route('/todo', methods=['POST'])
@token_required
def create_todo(current_user):
    data = request.json()

    new_todo = Todo(text=data['text'], complete=False, )
    db.session.add(new_todo)
    db.session.commit()

    return ''

@api_request.route('/todo/<todo_id>', methods=['PUT'])
@token_required
def complete_todo(current_user,todo_id):
    todo = Todo.query.filter_by(id = todo_id, user_id = current_user.id).first()

    if not todo: 
        return jsonify({'message': 'No todo found'})

    todo.complete = True
    db.session.commit()
    
    return jsonify({'message' : 'todo item has been completed!'})

@api_request.route('/todo/<todo_id>', methods=['DELETE'])
@token_required
def delete_todo(current_user,todo_id):
    todo = Todo.query.filter_by(id=todo_id, user_id = current_user.id).first()

    if not todo: 
        return jsonify({'message': 'No todo found'})
    
    db.session.delete(todo)
    db.session.commit()

    return jsonify({"message": "todo item deleted"})   


