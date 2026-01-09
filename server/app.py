#!/usr/bin/env python3

from flask import request, session
from flask_restful import Resource

from config import app, db, api
from models import User, UserSchema

class ClearSession(Resource):

    def delete(self):
    
        session['page_views'] = None
        session['user_id'] = None

        return {}, 204
    
class Signup(Resource):
    def post(self):
        # Get data from request body
        data = request.get_json()

        # Create a new user
        user = User(
            username=data['username']
        )

        # Set password using the password_hash setter
        user.password_hash = data['password']

        # Save user to the database
        db.session.add(user)
        db.session.commit()

        # Log in the user using session
        session['user_id'] = user.id

        # Serialize and return the user
        return UserSchema().dump(user), 201

class Login(Resource):
    def post(self):
        # Get login credentials from request body
        data = request.get_json()

        # Find the user by username
        user = User.query.filter(User.username == data.get('username')).first()

        # Verify user exists and password is correct
        if user and user.authenticate(data.get('password')):
            # Store user id in session to mark them as logged in
            session['user_id'] = user.id
            return UserSchema().dump(user), 200

        # Invalid credentials
        return {}, 401
class Logout(Resource):
    def delete(self):
        # Remove user id from session to log out the user
        session['user_id'] = None
        return {}, 204
    
class CheckSession(Resource):
    def get(self):
        # Check if user is logged in
        user_id = session.get('user_id')

        if user_id:
            user = User.query.get(user_id)
            return UserSchema().dump(user), 200

        # No active session
        return {}, 204

api.add_resource(ClearSession, '/clear', endpoint='clear')

api.add_resource(Signup, '/signup')

api.add_resource(Login, '/login')

api.add_resource(Logout, '/logout')

api.add_resource(CheckSession, '/check_session')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
