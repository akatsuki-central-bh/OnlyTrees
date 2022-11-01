import os
from app.database.database import get_db
from werkzeug.security import check_password_hash, generate_password_hash

class User():
    def __init__(self, username, password, role, id = None):
        self.id = id
        self.username = username
        self.password = password
        self.role = role

    def params_is_valid(function):
        def wrapper(ctx, username, password, role, fingerprint):
            if not username:
                raise Exception('Username is required.')
            elif not password:
                raise Exception('Password is required.')
            elif not role:
                raise Exception('Role is required.')

            return function(ctx, username, password, role, fingerprint)

        return wrapper

    @classmethod
    def find(cls, id):
        user_data = get_db().execute('SELECT * FROM users WHERE id = ?', (id,)).fetchone()

        if user_data is None:
            return False

        return User(
            id=user_data['id'],
            username=user_data['username'],
            password=user_data['password'],
            role=user_data['role']
        )

    @classmethod
    @params_is_valid
    def create(cls, username, password, role, fingerprint):
        db = get_db()
        cursor = db.cursor()

        password = generate_password_hash(password)

        try:
            cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, password, role,))

            db.commit()

            if not fingerprint is None:
                fingerprint.save(
                    os.path.join('app/database/images/user/fingerprints/',
                    f"{cursor.lastrowid}.BMP"))

            return User(
                id = cursor.lastrowid,
                username = username,
                password = password,
                role = role
            )

        except:
            return False

    # @params_is_valid
    def update(self, password, role, fingerprint):
        db = get_db()

        try:
            db.execute(
                'UPDATE users set password = ?, role = ? WHERE id = ?',
                (password, role, self.id)
            )

            fingerprint.save(
                os.path.join('app/database/images/user/fingerprints/',
                f"{id}.BMP"))

            db.commit()

            self.password = generate_password_hash(password)
            self.role = role

            return self
        except:
            return False

    def destroy():
        pass

    @classmethod
    def login(cls, username, password):
        db = get_db()
        user_data = db.execute(
            'SELECT * FROM users WHERE username = ?', (username,)
        ).fetchone()

        if user_data is None:
            return False

        if not check_password_hash(user_data['password'], password):
            return False

        return User(
            id=user_data['id'],
            username=user_data['username'],
            password=user_data['password'],
            role=user_data['role']
        )

    def exists_user():
        db = get_db()
        user_data = db.execute(
            'SELECT * FROM users limit 1').fetchone()

        return not user_data is None

    def compare_password(self, password):
        return check_password_hash(self.password, password)
