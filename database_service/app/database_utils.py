from database_model import db


def initialize_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
