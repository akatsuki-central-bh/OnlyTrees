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
            id=content_data['id'],
            title=content_data['title'],
            body=content_data['body']
        )
