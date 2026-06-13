from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token
from marshmallow import ValidationError

from app import db
from app.models.user import User
from app.schemas.user_schema import UserRegisterSchema, UserLoginSchema

auth_bp = Blueprint("auth", __name__)
bcrypt = Bcrypt()

register_schema = UserRegisterSchema()
login_schema = UserLoginSchema()


@auth_bp.route("/register", methods=["POST"])
def register():
    try:
        data = register_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify(err.messages), 400

    existing_user = User.query.filter_by(email=data["email"]).first()

    if existing_user:
        return jsonify({"message": "Email already exists"}), 409

    hashed_password = bcrypt.generate_password_hash(
        data["password"]
    ).decode("utf-8")

    user = User(
        name=data["name"],
        email=data["email"],
        password=hashed_password
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        data = login_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify(err.messages), 400

    user = User.query.filter_by(email=data["email"]).first()

    if not user:
        return jsonify({"message": "Invalid email or password"}), 401

    if not bcrypt.check_password_hash(user.password, data["password"]):
        return jsonify({"message": "Invalid email or password"}), 401

    access_token = create_access_token(identity=str(user.id))

    return jsonify({
        "message": "Login successful",
        "access_token": access_token
    }), 200


import os
import uuid
from werkzeug.utils import secure_filename
from flask import current_app
from flask_jwt_extended import jwt_required, get_jwt_identity

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@auth_bp.route("/profile-photo", methods=["POST"])
@jwt_required()
def upload_profile_photo():
    if 'photo' not in request.files:
        return jsonify({"message": "No photo file provided"}), 400
    
    file = request.files['photo']
    if file.filename == '':
        return jsonify({"message": "No photo file selected"}), 400
    
    if file and allowed_file(file.filename):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return jsonify({"message": "User not found"}), 404
            
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        
        upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
        file_path = os.path.join(upload_folder, unique_filename)
        file.save(file_path)
        
        if user.profile_photo:
            old_photo_path = os.path.join(upload_folder, user.profile_photo)
            if os.path.exists(old_photo_path):
                try:
                    os.remove(old_photo_path)
                except Exception:
                    pass
                    
        user.profile_photo = unique_filename
        db.session.commit()
        
        photo_url = f"/static/uploads/{unique_filename}"
        return jsonify({
            "message": "Profile photo uploaded successfully",
            "photo_url": photo_url,
            "filename": unique_filename
        }), 200
        
    return jsonify({"message": "Allowed file types are png, jpg, jpeg, gif, webp"}), 400


@auth_bp.route("/profile-photo", methods=["DELETE"])
@jwt_required()
def delete_profile_photo():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
        
    if user.profile_photo:
        upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
        photo_path = os.path.join(upload_folder, user.profile_photo)
        if os.path.exists(photo_path):
            try:
                os.remove(photo_path)
            except Exception:
                pass
        user.profile_photo = None
        db.session.commit()
        return jsonify({"message": "Profile photo removed successfully"}), 200
        
    return jsonify({"message": "No profile photo to delete"}), 400


@auth_bp.route("/profile-photo", methods=["GET"])
@jwt_required()
def get_profile_photo():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
        
    if user.profile_photo:
        photo_url = f"/static/uploads/{user.profile_photo}"
        return jsonify({
            "photo_url": photo_url,
            "filename": user.profile_photo
        }), 200
        
    return jsonify({"photo_url": None}), 200