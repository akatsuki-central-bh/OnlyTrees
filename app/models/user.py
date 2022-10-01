from app.database import get_db
from werkzeug.security import check_password_hash, generate_password_hash
class User():
    def __init__(self, username, password, role, id = None):
        self.id = id
        self.username = username
        self.password = password

    def params_is_valid(function):
        def wrapper(ctx, username, password, role):
            if not username:
                raise Exception('Username is required.')
            elif not password:
                raise Exception('Password is required.')
            elif not role:
                raise Exception('Role is required.')

            return function(ctx, username, password, role)

        return wrapper

    def find(self, id):
        pass

    @classmethod
    @params_is_valid
    def create(cls, username, password, role):
        db = get_db()
        cursor = db.cursor()

        password = generate_password_hash(password)

        try:
            cursor.execute(
                "INSERT INTO user (username, password, role) VALUES (?, ?, ?)",
                (username, password, role),
            )

            db.commit()

            return User(
                id = cursor.lastrowid,
                username = username,
                password = password,
                role = role
            )

        except:
            return False

    @params_is_valid
    def update(self, username, password, role):
        pass

    def destroy():
        pass

    @classmethod
    def login(cls, username, password):
        db = get_db()
        user_data = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
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
            'SELECT * FROM user limit 1').fetchone()

        return not user_data is None
