from app.database.database import get_db

class Content():
    def __init__(self, id, title, body):
        self.id = id
        self.title = title
        self.body = body

    @classmethod
    def find(cls, id):
        content_data = get_db().execute(
            'SELECT p.id, title, body'
            ' FROM post p JOIN user u ON p.author_id = u.id'
            ' WHERE p.id = ?',
            (id,)
        ).fetchone()

        if content_data is None:
            return False

        return Content(
            id = content_data['id'],
            title = content_data['title'],
            body = content_data['body']
        )

    @classmethod
    def create(cls, title, body):
        db = get_db()
        cursor = db.cursor()

        try:
            cursor.execute("INSERT INTO content (title, body) VALUES (?, ?)",
            (title, body,))

            db.commit()

            return Content(
                id = cursor.lastrowid,
                title = title,
                body = body
            )

        except:
            return False


    def update(self, title, body):
        try:
            db = get_db()
            db.execute(
                'UPDATE content SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, self.id)
            )

            self.title = title
            self.body = body

            return self
        except:
            return False

    def destroy(self):
        try:
            db = get_db()
            db.execute(
                'DELETE content WHERE id = ?', (self.id,)
            )

            return True
        except:
            return False
