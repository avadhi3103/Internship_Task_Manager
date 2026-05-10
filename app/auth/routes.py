from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app import db, bcrypt
from app.models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'username, email and password are required'}), 400
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'email already registered'}), 409
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'username already registered'}), 409
    
    hashed_pw = bcrypt.generate_password_hash(data['password']).decode('utf-8')

    user = User(
        username=data['username'],
        email=data['email'],
        password=hashed_pw
    )
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'user registered successfully', 'user': user.to_dict()}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data=request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'username, email and password are required'}), 400
    user = User.query.filter_by(email=data['email']).first()
    if not user or not bcrypt.check_password_hash(user.password, data['password']):
        return jsonify({'error': 'invalid'}), 401
    token = create_access_token(identity=str(user.id))
    
    return jsonify({'access_token': token, 'user': user.to_dict()}), 200

@auth_bp.route('/me',methods=['GET'])
@jwt_required()
def me():
    user_id=get_jwt_identity
    user = User.query.get(user_id)
    return jsonify(user.to_dict()), 200
