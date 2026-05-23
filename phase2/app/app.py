from flask import Flask
from models import db
from routes import users_bp
from seed import TableTemplate
import os

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DB_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    app.register_blueprint(users_bp)

    with app.app_context():
        db.drop_all()
        db.create_all()
        TableTemplate()
    
    return app


app = create_app()


if __name__ == "__main__":
    # app.run(debug=True)
    app.run(host="0.0.0.0", port=5000)

