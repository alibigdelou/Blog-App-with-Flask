from flask import Blueprint, request, jsonify
from app import db  
from app.models import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from .schema import UserSchema


auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if User.query.filter_by(email=data.get("email")).first():
        return jsonify({'msg': "Email already exists!"})
    
    firstname = data.get('firstname')
    lastname = data.get('lastname')
    username = data.get('username')
    email = data.get('email')
    user = User(firstname=firstname, lastname=lastname, username=username, email=email)
    user.set_password(password=data.get('password'))
    db.session.add(user)
    db.session.commit()
    return jsonify('User registered successfully! ')

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    print(data)
    user = User.query.filter_by(username=data.get('username')).first()
    print(user)
    if user and user.check_password(data.get('password')):
        access_token = create_access_token(identity=str(user.uid))
        return jsonify({'access_token': access_token})
    else:
        return jsonify({'msg': 'Invalid Credentials!'})
    

@auth_bp.route('/profile')
@jwt_required()
def user_profile():
    current_user = int(get_jwt_identity())
    
    user_profile = User.query.filter_by(uid=current_user).first()
    result = UserSchema().dump({
        'uid': user_profile.uid,
        'firstname': user_profile.firstname,
        'lastname': user_profile.lastname,
        'username': user_profile.username,
        'email': user_profile.email

    })
    return jsonify(result)
    
