from app import app
from model import db, User
from werkzeug.security import generate_password_hash

with app.app_context():
    if not User.query.filter_by(email="amjadkhanpathan1980@gmail.com").first():
        new_admin = User(
            name="Admin",
            email="amjadkhanpathan1980@gmail.com",
            password=generate_password_hash("amjad098"),
            is_admin=True
        )
        db.session.add(new_admin)
        db.session.commit()
        print("ADMIN CREATED")
    else:
        print("ADMIN ALREADY EXISTS")
