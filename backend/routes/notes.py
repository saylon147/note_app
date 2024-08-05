from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.models import Note, TextNote, User


notes = Blueprint('notes', __name__)

ERROR_CODES = {
    404: "Not Found",
    500: "Internal Server Error",
}


def create_response(message, status_code):
    return (jsonify({"msg": message, "status": status_code,
                    "error": ERROR_CODES.get(status_code, "")}),
            status_code)


@notes.route('/notes', methods=['POST'])
@jwt_required()
def create_note():
    try:
        user_id = get_jwt_identity()
        user = User.objects(id=user_id).first()

        if not user:
            return create_response("User not found", 404)

        data = request.get_json()
        title = data.get('title')
        content = data.get('content')
        tags = data.get('tags')

        note = TextNote(user=user, title=title, content=content, tags=tags)
        note.save()

        return jsonify({"msg": "Note created successfully"}), 201
    except Exception as e:
        current_app.logger.error(f"Error creating note: {str(e)}")
        return create_response("Internal Server Error", 500)


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
