from app.database.database import get_db

class Content():
    def __init__(self, id, title, body, access_level):
        self.id = id
        self.title = title
        self.body = body
        self.access_level = access_level

    @classmethod
    def all(cls):
        db = get_db()

        contents = db.execute('SELECT * FROM contents').fetchall()

        return map(lambda result: Content(
            id=result['id'],
            title=result['title'],
            body=result['body'],
            access_level=result['access_level']
        ), contents)


    @classmethod
    def find(cls, id):
        content_data = get_db().execute(
            'SELECT *'
            ' FROM contents'
            ' WHERE id = ?',
            (id,)
        ).fetchone()

        if content_data is None:
            return False

        return Content(
            id = content_data['id'],
            title = content_data['title'],
            body = content_data['body'],
            access_level = content_data['access_level']
        )

    @classmethod
    def create(cls, title, body, access_level):
        db = get_db()
        cursor = db.cursor()

        try:
            cursor.execute(
                "INSERT INTO contents (title, body, access_level) VALUES (?, ?, ?)",
                (title, body, access_level)
            )

            db.commit()

            return Content(
                id = cursor.lastrowid,
                title = title,
                body = body,
                access_level = access_level
            )

        except:
            return False


    def update(self, title, body, access_level):
        try:
            db = get_db()
            db.execute(
                'UPDATE contents SET title = ?, body = ?, access_level = ?'
                ' WHERE id = ?',
                (title, body, access_level, self.id)
            )

            db.commit()

            self.title = title
            self.body = body
            self.access_level = access_level

            return self
        except:
            return False

    def destroy(self):
        try:
            db = get_db()
            db.execute('DELETE FROM contents WHERE id = ?', (self.id,))

            db.commit()

            return True
        except:
            return False

    def is_permitted(self, role):
        if role is None and self.access_level == 2:
            return True

        if role == 1:
            return True

        if self.access_level <= role:
            return True

        return False
