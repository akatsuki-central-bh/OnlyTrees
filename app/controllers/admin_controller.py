import functools
import os

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from app.models.fingerprint import FingerPrint

bp = Blueprint('admin', __name__, url_prefix='/admin')

from .auth_controller import login_required

def admin_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user.role == 1:
            flash('você não tem permissão para acessar essa página')
            return redirect(url_for('index'))

        return view(**kwargs)

    return wrapped_view

@bp.route('/invite', methods=['GET'])
@admin_required
def new_user():
    return render_template('auth/invite.html')

@bp.route('/invite', methods=['POST'])
@admin_required
def create_user():
    username = request.form['username']
    flash(username)
    return render_template('auth/invite.html')

@admin_required
@bp.route('/edit', methods=['GET'])
def edit_user():
    pass

@admin_required
@bp.route('/edit', methods=['POST'])
def update_user():
    pass
