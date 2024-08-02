from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.models import Note, User

notes = Blueprint('notes', __name__)


@notes.route('/notes', methods=['POST'])
@jwt_required()
def create_note():
    user_id = get_jwt_identity()
    user = User.objects(id=user_id).first()

    data = request.get_json()
    title = data.get('title')
    content = data.get('content')
    tags = data.get('tags')

    note = Note(user=user, title=title, content=content, tags=tags)
    note.save()

    return jsonify({"msg": "Note created successfully"}), 201


@notes.route('/notes', methods=['GET'])
@jwt_required()
def get_notes():
    user_id = get_jwt_identity()
    user = User.objects(id=user_id).first()

    notes = Note.objects(user=user)
    notes_data = [{"title": note.title,
                   "content": note.content,
                   "tags": note.tags,
                   "create_time": note.created_at,
                   "update_time": note.updated_at,}
                  for note in notes]

    return jsonify(notes_data), 200
