from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson.objectid import ObjectId
from extensions import mongo
import datetime

notes_bp = Blueprint('notes', __name__)

@notes_bp.route('/', methods=['POST'])
@jwt_required()
def create_note():
    user_id = get_jwt_identity()
    data = request.get_json()
    note_id = mongo.db.notes.insert_one({
        'user_id': ObjectId(user_id),
        'title': data['title'],
        'content': data['content'],
        'created_at': datetime.datetime.utcnow(),
        'updated_at': datetime.datetime.utcnow()
    }).inserted_id
    return jsonify(message="Note created", note_id=str(note_id)), 201

@notes_bp.route('/', methods=['GET'])
@jwt_required()
def get_notes():
    user_id = get_jwt_identity()
    notes = list(mongo.db.notes.find({'user_id': ObjectId(user_id)}))
    for note in notes:
        note['_id'] = str(note['_id'])
        note['user_id'] = str(note['user_id'])
    return jsonify(notes)
