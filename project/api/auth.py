# project/api/auth.py


from flask import Blueprint, jsonify, request, make_response
from sqlalchemy import exc, or_

from project.api.models import User
from project import db, bcrypt


auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/auth/register', methods=['POST'])
def register_user():
    # get post data
    post_data = request.get_json()
    if not post_data:
        response_object = {
            'status': 'error',
            'message': 'Invalid payload.'
        }
        return make_response(jsonify(response_object)), 400
    username = post_data.get('username')
    email = post_data.get('email')
    password = post_data.get('password')
    try:
        # check for existing user
        user = User.query.filter(
            or_(User.username == username, User.email==email)).first()
        if not user:
            # add new user to db
            new_user = User(
                username=username,
                email=email,
                password=password
            )
            db.session.add(new_user)
            db.session.commit()
            # generate auth token
            auth_token = new_user.encode_auth_token(new_user.id)
            response_object = {
                'status': 'success',
                'message': 'Successfully registered.',
                'auth_token': auth_token.decode()
            }
            return make_response(jsonify(response_object)), 201
        else:
            response_object = {
                'status': 'error',
                'message': 'Sorry. That user already exists.'
            }
            return make_response(jsonify(response_object)), 400
    # handler errors
    except exc.IntegrityError as e:
        db.session().rollback()
        response_object = {
            'status': 'error',
            'message': 'Invalid payload.'
        }
        return make_response(jsonify(response_object)), 400
    except ValueError as e:
        db.session().rollback()
        response_object = {
            'status': 'error',
            'message': 'Invalid payload.'
        }
        return make_response(jsonify(response_object)), 400


@auth_blueprint.route('/auth/login', methods=['POST'])
def login_user():
    # get post data
    post_data = request.get_json()
    if not post_data:
        response_object = {
            'status': 'error',
            'message': 'Invalid payload.'
        }
        return make_response(jsonify(response_object)), 400
    email = post_data.get('email')
    password = post_data.get('password')
    try:
        # fetch the user data
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            auth_token = user.encode_auth_token(user.id)
            if auth_token:
                response_object = {
                    'status': 'success',
                    'message': 'Successfully logged in.',
                    'auth_token': auth_token.decode()
                }
                return make_response(jsonify(response_object)), 200
        else:
            response_object = {
                'status': 'error',
                'message': 'User does not exist.'
            }
            return make_response(jsonify(response_object)), 404
    except Exception as e:
        print(e)
        response_object = {
            'status': 'error',
            'message': 'Try again.'
        }
        return make_response(jsonify(response_object)), 500


@auth_blueprint.route('/auth/logout', methods=['GET'])
def logout_user():
    # get auth token
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
        resp = User.decode_auth_token(auth_token)
        if not isinstance(resp, str):
            response_object = {
                'status': 'success',
                'message': 'Successfully logged out.'
            }
            return make_response(jsonify(response_object)), 200
        else:
            response_object = {
                'status': 'error',
                'message': resp
            }
            return make_response(jsonify(response_object)), 401
    else:
        response_object = {
            'status': 'error',
            'message': 'Provide a valid auth token.'
        }
        return make_response(jsonify(response_object)), 403


@auth_blueprint.route('/auth/status', methods=['GET'])
def get_user_status():
    # get auth token
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
        resp = User.decode_auth_token(auth_token)
        if not isinstance(resp, str):
            user = User.query.filter_by(id=resp).first()
            response_object = {
                'status': 'success',
                'data': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'active': user.active,
                    'created_at': user.created_at
                }
            }
            return make_response(jsonify(response_object)), 200
        response_object = {
            'status': 'error',
            'message': resp
        }
        return make_response(jsonify(response_object)), 401
    else:
        response_object = {
            'status': 'error',
            'message': 'Provide a valid auth token.'
        }
        return make_response(jsonify(response_object)), 401
