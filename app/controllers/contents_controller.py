from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from .auth_controller import login_required
from app.database.database import get_db
from app.models.content import Content

bp = Blueprint('contents', __name__)

@bp.route('/')
def index():
    contents = Content.all()

    role = None
    if g.user:
        role = g.user.role

    if g.user:
        allowed_contents = filter(
            lambda content: ( content.is_permitted(role) ),
            contents
        )
    else:
        allowed_contents = filter(
            lambda content: (content.access_level == 2),
            contents
        )

    return render_template('contents/index.html', contents=allowed_contents)

@bp.route('/create', methods=['GET'])
@login_required
def new():
    return render_template('contents/create.html')

@bp.route('/create', methods=['POST'])
@login_required
def create():
    title = request.form['title']
    body = request.form['body']
    access_level = request.form['access_level']

    content = Content.create(title, body, access_level)
    if not content:
        flash('Falha ao tentar publicar conteúdo')
        return render_template('contents/create.html')

    return redirect(url_for('contents.index'))

@bp.route('/<int:id>', methods=['GET'])
def show(id):
    content = Content.find(id)

    if not content:
        flash('Conteúdo não encontrado')
        return redirect(url_for('contents.index'))

    role = None
    if g.user:
        role = g.user.role

    if not (content.is_permitted(role)):
        flash('Você não tem permissão para ver o conteúdo')
        return redirect(url_for('contents.index'))

    return render_template('contents/show.html', content=content)

@bp.route('/<int:id>/edit', methods=['GET'])
@login_required
def edit(id):
    content = Content.find(id)

    role = None
    if g.user:
        role = g.user.role

    if not (content.is_permitted(role)):
        flash('Você não tem permissão para ver o conteúdo')
        return redirect(url_for('contents.index'))

    return render_template('contents/edit.html', content=content)

@bp.route('/<int:id>/edit', methods=['POST'])
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
        content = content.update(title, body, access_level)

        if content is False:
            flash('Falha ao tentar editar conteúdo')
            return redirect(url_for('contents.edit', id=id))

        return redirect(url_for('contents.index'))


@bp.route('/<int:id>/delete', methods=['GET'])
@login_required
def delete(id):
    content = Content.find(id)

    if not content:
        flash('Alteração inválida')
        return redirect(url_for('contents.index'))

    if content.destroy():
        flash('Conteúdo excluído com sucesso')
        return redirect(url_for('contents.index'))
    else:
        flash('Falha ao tentar excluir conteúdo')
        return redirect(url_for('contents.index'))
