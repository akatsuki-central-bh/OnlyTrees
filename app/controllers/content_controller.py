from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from .auth_controller import login_required
from app.database.database import get_db
from app.models.content import Content

bp = Blueprint('content', __name__)

@bp.route('/')
def index():
    # db = get_db()
    # posts = db.execute(
    #     'SELECT p.id, title, body, created, author_id, username'
    #     ' FROM post p JOIN user u ON p.author_id = u.id'
    #     ' ORDER BY created DESC'
    # ).fetchall()
    return render_template('content/index.html')

@bp.route('/new', methods=['GET'])
@login_required
def new():
    return render_template('content/new.html')

@bp.route('/create', methods=['POST'])
@login_required
def create():
    title = request.form['title']
    body = request.form['body']
    access_level = request.form['access_level']

    content = Content.create(title, body, access_level)
    if not content:
        flash('Falha ao tentar publicar conteúdo')
        return render_template('content/new.html')

    return redirect(url_for('content.index'))


@bp.route('/<int:id>/edit', methods=['GET'])
def edit(id):
    content = Content.find(id)
    return render_template('content/update.html', content=content)

@bp.route('/<int:id>/update', methods=['POST'])
@login_required
def update(id):
    title = request.form['title']
    body = request.form['body']
    access_level = request.form['access_level']

    error = None

    if not title:
        error = 'Title is required.'

    if error is not None:
        flash(error)
    else:
        content = Content.find(id)
        content.update(title, body, access_level)

        return redirect(url_for('content.index'))


@bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    content = Content.find(id)

    if not content:
        flash('Alteração inválida')
        return redirect(url_for('content.index'))

    content.destroy()
