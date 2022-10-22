import functools
import os

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from app.models.fingerprint import FingerPrint

bp = Blueprint('auth', __name__, url_prefix='/auth')

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'upload')

from app.models.user import User

@bp.route('/register', methods=['GET'])
def new_register():
    return render_template('auth/register.html')

@bp.route('/register', methods=['POST'])
def create_register():
    fingerprint = request.files['file']

    username = request.form['username']
    password = request.form['password']

    user = User.create(username, password, 1, fingerprint)

    if not user:
        flash('usuário já cadastrado')
        return render_template('auth/register.html')

    flash('usuário criado com sucesso')
    return redirect(url_for("auth.new_session"))

@bp.route('/edit', methods=['GET'])
@login_required
def edit_user():
    return render_template('auth/edit.html')

@bp.route('/register', methods=['PATCH'])
def update_user():
    fingerprint = request.files['file']

    user = User.find(g.user)

    id = session.get('user_id')
    username = request.form['username']
    current_password = request.form['current_password']
    new_password = request.form['new_password']
    confirm_password = request.form['confirm_password']

    user = User.compare_password(current_password)

    role = request.form['role']

    if current_password != confirm_password:
        flash('senhas não coincidem')
        return render_template('auth/edit.html')

    user = User.update(id, username, new_password, role, fingerprint)

    if not user:
        flash('Alteração inválida')
        return render_template('auth/edit.html')

    flash('Alterado com sucesso')
    return redirect(url_for('index'))

@bp.route('/login', methods=['GET'])
def new_session():
    return render_template('auth/login.html')

@bp.route('/login', methods=['POST'])
def create_session():
    username = request.form['username']
    password = request.form['password']
    fingerprint = request.files['file']

    user = None

    if not request.files.get('file', None):
        user = User.login(username, password)
    else:
        user = login_with_fingerprint(fingerprint)

    if not user:
        flash('login inválido')
        return render_template('auth/login.html')

    session.clear()
    session['user_id'] = user.id
    return redirect(url_for('index'))

def login_with_fingerprint(fingerprint):
    filename = fingerprint.filename
    fingerprint.save(f'app/temp/{filename}')

    command = FingerPrint(f'app/temp/{filename}')
    id_user = command.call()

    flash(f'best_score: {command.best_score}, image: {command.filename}')

    os.remove(f'app/temp/{filename}')

    return User.find(id_user)

@bp.route('/logout')
def delete_session():
    session.clear()
    return redirect(url_for('index'))

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = User.find(user_id)

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.new_session'))

        return view(**kwargs)

    return wrapped_view
