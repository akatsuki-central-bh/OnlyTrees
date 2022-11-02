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
        if g.user.role != 1:
            flash('você não tem permissão para acessar essa página')
            return redirect(url_for('index'))

        return view(**kwargs)

    return wrapped_view

@bp.route('/invite', methods=['GET'])
@admin_required
def new_user():
    users = User.all()
    return render_template('auth/invite.html', users=users)

@bp.route('/invite', methods=['POST'])
@admin_required
def create_user():
    username = request.form['username']
    role = request.form['perfil']
    password = "admin123"
    flash(username)
    User.create(username, password, role, None)
    return render_template('auth/invite.html')

@admin_required
@bp.route('/edit', methods=['GET'])
def edit_user():
    pass

@admin_required
@bp.route('/edit', methods=['POST'])
def update_user():
    pass
