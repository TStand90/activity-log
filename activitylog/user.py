from werkzeug.security import generate_password_hash, check_password_hash


class User:

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.set_hashed_password(password)

    def set_hashed_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)
