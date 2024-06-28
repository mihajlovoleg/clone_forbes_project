from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, TextAreaField, IntegerField, EmailField, SelectField, HiddenField
from wtforms.validators import DataRequired, Email
from flask_wtf.file import FileAllowed

class RegistrationForm(FlaskForm):
    name = StringField('First name', validators=[DataRequired()])
    surname = StringField('Last name', validators=[DataRequired()])
    login = StringField('Login', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')
    
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')

class ForgotPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')
    
class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Submit')
    
    
class CreateArticleForm(FlaskForm):
    main_image = FileField('Add main article image:', validators=[
        DataRequired(),
        FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')
    ])
    art_title = StringField('Add title of your article:', validators=[DataRequired()])
    content = TextAreaField('', validators=[DataRequired()])
    submit = SubmitField('Submit')

class EditArticleForm(FlaskForm):
    main_image = FileField('Add main article image:', validators=[
        DataRequired(),
        FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')
    ])
    art_title = StringField('Add title of your article:', validators=[DataRequired()])
    content = TextAreaField('', validators=[DataRequired()])
    submit = SubmitField('Submit')
    
    
class AdminForm(FlaskForm):
    user_id = IntegerField()
    name = StringField('Name')
    surname = StringField('Surname')
    password = StringField('Password')
    email = EmailField('Email')
    role = SelectField('Role', choices=[('admin', 'Admin'), ('moder', 'Moderator'), ('user', 'Viewer')])
    submit = SubmitField('Save')

class DeleteForm(FlaskForm):
    csrf_token = HiddenField()