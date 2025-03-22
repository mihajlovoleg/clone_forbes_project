from flask import Blueprint, render_template, redirect, url_for
from app.forms import ForgotPasswordForm, ResetPasswordForm
from app.models import User
from app import db
from app.utils import send_email
from itsdangerous import URLSafeTimedSerializer
from app.config import SECRET_KEY

pw_bp = Blueprint('pw', __name__)
s = URLSafeTimedSerializer(secret_key=SECRET_KEY)

@pw_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            return redirect(url_for('auth.sign_in'))
        
        token = s.dumps(form.email.data, salt='password-reset-salt')
        link = url_for('pw.reset_password', token=token, _external=True)
        send_email(form.email.data, 'Password Reset Request', f"<p>Hello<br>Click the link to reset your password: <a href='{link}'>Reset Password</a></p>")
        return redirect(url_for('auth.sign_in'))
    
    return render_template('password_templates/forgot_password.html', form=form)

@pw_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    form = ResetPasswordForm()
    
    try:
        email = s.loads(token, salt='password-reset-salt', max_age=3600)
    except:
        print("Invalid or expired token.")
    

    
    
    if form.validate_on_submit():
        user = User.query.filter_by(email=email).first()
        print(user)
        if user:
            user.password = form.password.data
            db.session.commit()
            return redirect(url_for('auth.sign_in'))
        
    
    return render_template('password_templates/reset_password.html', form=form, token=token)
