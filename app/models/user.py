from app.database import get_db
class User():
    def __init__(self, username, password, id = None):
        self.id = id
        self.username = username
        self.password = password

    def find(self, id):
        pass

    @classmethod
    def create(cls, username, password, role):
        db = get_db()
        cursor = db.cursor()

        try:
            cursor.execute(
                "INSERT INTO user (username, password, role) VALUES (?, ?, ?)",
                (username, password, role),
            )

            db.commit()

            return User(
                id = cursor.lastrowid,
                username = username,
                password = password)

        except:
            return False

    def update():
        pass

    def destroy():
        pass
