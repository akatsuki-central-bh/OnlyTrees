import functools
import os

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

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

@bp.route('/login', methods=['GET'])
def new_session():
    return render_template('auth/login.html')

@bp.route('/login', methods=['POST'])
def create_session():
    username = request.form['username']
    password = request.form['password']

    user = User.login(username, password)

    if not user:
        flash('login inválido')
        return render_template('auth/login.html')

    session.clear()
    session['user_id'] = user.id
    return redirect(url_for('index'))

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
