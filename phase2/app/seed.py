from models import db, User


def TableTemplate():
    if User.query.count() == 0:
        db.session.add(User(name="John", email="abc@123", password="123"))
        db.session.add(User(name="Jane", email="def@456", password="456"))
        db.session.add(User(name="Doe", email="ghi@789", password="789"))
        db.session.commit()
    return