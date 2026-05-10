from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db, socketio
from app.models import Task

tasks_bp = Blueprint('tasks', __name__)


@tasks_bp.route('/', methods=['GET'])
@jwt_required()
def get_tasks():
    user_id = get_jwt_identity()
    tasks = Task.query.filter_by(user_id=user_id).all()
    return jsonify([t.to_dict() for t in tasks]), 200


@tasks_bp.route('/', methods=['POST'])
@jwt_required()
def add_task():
    user_id = get_jwt_identity()
    data = request.get_json()

    if not data or not data.get('title'):
        return jsonify({'error': 'title is required'}), 400

    task = Task(
        user_id=user_id,
        title=data['title'],
        description=data.get('description', ''),
        priority=data.get('priority', 'medium'),
        status=data.get('status', 'pending')
    )
    db.session.add(task)
    db.session.commit()

    socketio.emit('task_updated', task.to_dict(), room=f"user_{user_id}")

    return jsonify(task.to_dict()), 201


@tasks_bp.route('/<int:id>', methods=['PATCH'])
@jwt_required()
def update_task(id):
    user_id = get_jwt_identity()
    task = Task.query.filter_by(id=id, user_id=user_id).first()

    if not task:
        return jsonify({'error': 'task not found'}), 404

    data = request.get_json()

    if data.get('title'):
        task.title = data['title']
    if data.get('description'):
        task.description = data['description']
    if data.get('priority'):
        task.priority = data['priority']
    if data.get('status'):
        task.status = data['status']

    db.session.commit()

    socketio.emit('task_updated', task.to_dict(), room=f"user_{user_id}")

    return jsonify(task.to_dict()), 200


@tasks_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_task(id):
    user_id = get_jwt_identity()
    task = Task.query.filter_by(id=id, user_id=user_id).first()

    if not task:
        return jsonify({'error': 'task not found'}), 404

    db.session.delete(task)
    db.session.commit()

    socketio.emit('task_deleted', {'id': id}, room=f"user_{user_id}")

    return jsonify({'message': 'task deleted'}), 200