import os
from app.database.database import get_db
from werkzeug.security import check_password_hash, generate_password_hash

class User():
    def __init__(self, email, password, role, id = None):
        self.id = id
        self.email = email
        self.password = password
        self.role = role

    def params_is_valid(function):
        def wrapper(ctx, email, password, role, fingerprint):
            if not email:
                raise Exception('email is required.')
            elif not password:
                raise Exception('Password is required.')
            elif not role:
                raise Exception('Role is required.')

            return function(ctx, email, password, role, fingerprint)

        return wrapper

    @classmethod
    def find(cls, id):
        user_data = get_db().execute('SELECT * FROM users WHERE id = ?', (id,)).fetchone()

        if user_data is None:
            return False

        return User(
            id=user_data['id'],
            email=user_data['email'],
            password=user_data['password'],
            role=user_data['role']
        )

    @classmethod
    def all(cls):
        db = get_db()

        users = db.execute('SELECT * FROM users').fetchall()

        return map(lambda result: User(
            id=result['id'],
            email=result['email'],
            password=result['password'],
            role=result['role']
        ), users)

    @classmethod
    @params_is_valid
    def create(cls, email, password, role, fingerprint):
        db = get_db()
        cursor = db.cursor()

        password = generate_password_hash(password)

        try:
            cursor.execute("INSERT INTO users (email, password, role) VALUES (?, ?, ?)", (email, password, role,))

            db.commit()

            if not fingerprint is None:
                fingerprint.save(
                    os.path.join('app/database/images/user/fingerprints/',
                    f"{cursor.lastrowid}.BMP"))

            return User(
                id = cursor.lastrowid,
                email = email,
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
    def login(cls, email, password):
        db = get_db()
        user_data = db.execute(
            'SELECT * FROM users WHERE email = ?', (email,)
        ).fetchone()

        if user_data is None:
            return False

        if not check_password_hash(user_data['password'], password):
            return False

        return User(
            id=user_data['id'],
            email=user_data['email'],
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

    @classmethod
    def admin_user_update(cls, role, userid, email = ""):
        db = get_db()

        try :

            if (email != ""):
                db.execute(
                    'UPDATE users SET email = ?, role = ? WHERE id = ?',
                    (email, role, userid)
                )

                db.commit()

                return True

            db.execute(
                'UPDATE users SET role = ? WHERE id = ?',
                (role, userid)
            )

            db.commit()

            return True
        except:
            return False

    @classmethod
    def count_admins():
        db = get_db()

        return db.execute('SELECT COUNT(*) FROM users WHERE role = 1').fetchone()[0]
