from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Task
import pandas as pd
import numpy as np

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/', methods=['GET'])
@jwt_required()
def get_analytics():
    user_id = get_jwt_identity()
    tasks = Task.query.filter_by(user_id=user_id).all()

    if not tasks:
        return jsonify({
            'total': 0,
            'completed': 0,
            'pending': 0,
            'in_progress': 0,
            'completion_percentage': 0.0
        }), 200

    df = pd.DataFrame([t.to_dict() for t in tasks])

    total       = len(df)
    completed   = int((df['status'] == 'completed').sum())
    pending     = int((df['status'] == 'pending').sum())
    in_progress = int((df['status'] == 'in_progress').sum())
    completion_pct = round(float(np.mean(df['status'] == 'completed') * 100), 2)

    priority_breakdown = df['priority'].value_counts().to_dict()

    return jsonify({
        'total': total,
        'completed': completed,
        'pending': pending,
        'in_progress': in_progress,
        'completion_percentage': completion_pct,
        'priority_breakdown': priority_breakdown
    }), 200