from sqlalchemy.ext.hybrid import hybrid_property
from marshmallow import Schema, fields

from config import db, bcrypt

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    _password_hash = db.Column(db.String)

    # Build method to protect password_hash property
    @hybrid_property
    def password_hash(self):
        # Prevent password hash from being accessed
        raise Exception("Password hashes may not be viewed.")

    # Build method to set password hash property using bcrypt.generate_password_hash()
    @password_hash.setter
    def password_hash(self, password):
        # Hash the password and store it securely
        hashed_password = bcrypt.generate_password_hash(password.encode('utf-8'))
        self._password_hash = hashed_password.decode('utf-8')

    # Build authenticate method that uses bcrypt.check_password_hash()
    def authenticate(self, password):
        # Check if the provided password matches the stored hash
        return bcrypt.check_password_hash(
        self._password_hash,
        password.encode('utf-8')
    )

    def __repr__(self):
        return f'User {self.username}, ID: {self.id}'

class UserSchema(Schema):
    id = fields.Int()
    username = fields.String()