from flask import Blueprint, jsonify, request
from models import db, User
import jwt, os
from datetime import datetime, timedelta

SECRET_KEY = os.getenv("SECRET_KEY")

users_bp = Blueprint("users", __name__)




@users_bp.route("/users", methods=["GET", "POST"], strict_slashes=False)
def users_route():
    method = request.method
    users = User.query.all()


    if method == "GET":
        return jsonify([u.to_dict() for u in users])


    name = request.json.get("name")
    email = request.json.get("email")
    if not name or not email:
        return jsonify({"error": "name and email are required"}), 400


    if method == "POST":
        if User.query.filter_by(email=email).first():
            return jsonify({"error": "email already exists"}), 400

        new_user = User(name=name, email=email) 
        db.session.add(new_user)
        db.session.commit()

        return jsonify(new_user.to_dict()), 201
    

@users_bp.route("/users/<int:id>", methods=["GET", "PUT", "DELETE"], strict_slashes=False)
def user_route(id):
    method = request.method
    if not User.query.get(id):
        return jsonify({"error": "user not found"}), 404
    user = User.query.get(id)

    if method == "GET":
        return jsonify(user.to_dict())


    if method =="DELETE":
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "user deleted successfully"}), 200


    name = request.json.get("name")
    email = request.json.get("email")
    if not name or not email:
        return jsonify({"error": "name and email are required"}), 400

        
    if method == "PUT":
        if User.query.filter_by(email=email).first() and user.email != email:
            return jsonify({"error": "email already exists"}), 400
        if user.email == email and user.name == name:
            return jsonify({"error": "no changes to update"}), 400
        user.name = name
        user.email = email
        db.session.commit()
        return jsonify(user.to_dict()), 200


@users_bp.route("/users/login", methods=["POST"], strict_slashes=False)
def login_route():
    method = request.method
    
    email = request.json.get("email")
    pwd = request.json.get("password")

    if method == "POST":
        if not email or not pwd:
            return jsonify({"error": "email and password are required"}), 400

        if User.query.filter_by(email=email, password=pwd).first():
            user = User.query.filter_by(email=email, password=pwd).first()
            token = jwt.encode(
                {
                    "sub": str(user.id),
                    "exp": datetime.utcnow() + timedelta(hours=1)
                },
                SECRET_KEY,
                algorithm="HS256"
            )

            return jsonify({"access_token": token}), 200
        
        return jsonify({"error": "invalid email or password"}), 401


@users_bp.route("/users/profile", methods=["GET"], strict_slashes=False)
def profile_route():
    method = request.method

    if method == "GET":
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({"error": "missing token"}), 401

        token = auth_header.split(" ")[1]

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user = User.query.get(payload["sub"])
            return jsonify({"message": "access granted",
                            "payload": payload,
                            "user": user.to_dict()})
        
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "token expired"}), 401

        except jwt.InvalidTokenError:
            return jsonify({"error": "invalid token"}), 401
    