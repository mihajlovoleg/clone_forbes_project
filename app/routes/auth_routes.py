from flask import Blueprint, render_template, redirect, url_for, flash, session
from app.forms import RegistrationForm, LoginForm
from app.models import User
from app import db
from app.utils import send_email



auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/signin", methods=['GET', 'POST'])
def sign_in():
    
    form = LoginForm()
    if form.validate_on_submit():
        
        user = User.query.filter_by(email=form.email.data, password=form.password.data).first()
        
        session['name'] = user.name
        session['surname'] = user.surname
        session['email'] = user.email
        session['role'] = user.role
        print(session.get('role'))
        if user is None:
            return redirect(url_for('auth.sign_in'))
        return redirect(url_for('home.home_page'))
    return render_template('users_templates/sign_in.html', form=form)

@auth_bp.route('/signup', methods=['GET', 'POST'])
def sign_up():
    form = RegistrationForm()
    if form.validate_on_submit():
        
        name = form.name.data
        surname = form.surname.data
        login = form.login.data
        password = form.password.data
        email = form.email.data
        role = 'user'
        
        new_user = User(
            name=name,
            surname=surname,
            login=login,
            password=password,
            email=email,
            role=role
        )
        try:
            db.session.add(new_user)
            db.session.commit()
            send_email(to_email=email, subject='Welcome to Forbes!', content='<p>Welcome to our service!<br>We glad to see you!</p>')
            return redirect(url_for('auth.sign_in'))
        except Exception as e:
            
            db.session.rollback()
            print(f"Error occurred: {str(e)}")
            
            return render_template('users_templates/sign_up.html', form=form, error=str(e))
       

    return render_template('users_templates/sign_up.html', form=form)

@auth_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    session['email'] = None
    session['name'] = None
    session['surname'] = None
    session['login'] = None
    session['password'] = None
    session['role'] = 'guest'
    return redirect(url_for('home.home_page'))