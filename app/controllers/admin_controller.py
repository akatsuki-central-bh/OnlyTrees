import functools
import os

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from app.models.fingerprint import FingerPrint
from app.models.user import User

bp = Blueprint('admin', __name__, url_prefix='/admin')

from .auth_controller import login_required

def admin_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            flash('você não está logado')
            return redirect(url_for('index'))
        if g.user.role != 1:
            flash('você não tem permissão para acessar essa página')
            return redirect(url_for('index'))

        return view(**kwargs)

    return wrapped_view

@bp.route('/', methods=['GET'])
@admin_required
def new_user():
    users = User.all()
    return render_template('admin/index.html', users=users)

@bp.route('/', methods=['POST'])
@admin_required
def create_user():
    username = request.form['username']
    role = request.form['perfil']
    password = "admin123"
    User.create(username, password, role, None)
    return redirect(url_for('admin.new_user'))

@admin_required
@bp.route('/<int:id>/edit', methods=['GET'])
def edit_user(id):
    user = User.find(id)
    return render_template('admin/edit.html', user=user)

@admin_required
@bp.route('/<int:id>/edit', methods=['POST'])
def update_user(id):
    username = request.form['username']
    role = request.form['perfil']
    userid = id
    User.admin_user_update(role=role, userid=userid, username=username)
    return redirect(url_for('admin.new_user'))
