from flask_socketio import join_room, emit
from flask_jwt_extended import decode_token
from app import socketio

@socketio.on('connect')
def handle_connect(auth):
    if not auth or not auth.get('token'):
        return False  # reject connection

    try:
        decoded = decode_token(auth['token'])
        user_id = decoded['sub']
        join_room(f"user_{user_id}")
        emit('connected', {'message': f'joined room user_{user_id}'})
    except Exception as e:
        return False  # reject if token invalid


@socketio.on('disconnect')
def handle_disconnect():
    pass