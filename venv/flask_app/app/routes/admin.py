from flask import Blueprint, render_template, redirect, url_for, request, session
from app.models import User
from app import db
from app.forms import AdminForm
from app.utils import is_admin

admin_bp = Blueprint('adm', __name__)

@admin_bp.route('/admin', methods=['GET', 'POST'])
def admin():
    print(type(session.get('role')))
    print(is_admin(session.get('role')))
    if not is_admin(session.get('role')):
        print('Arent admin')
        return redirect(url_for('home.home_page'))
        
    users = User.query.all()
    form = AdminForm()

    if form.validate_on_submit():
        user_id = form.user_id.data
        new_username = form.name.data
        new_surname = form.surname.data
        new_password = form.password.data
        new_email = form.email.data
        new_role = form.role.data

        user = User.query.get(user_id)
        if user:
            user.name = new_username
            user.surname = new_surname
            user.password = new_password
            user.email = new_email
            user.role = new_role
            db.session.commit()
            return redirect(url_for('adm.admin'))

    return render_template('admin.html', users=users, form=form)