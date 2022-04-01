from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password2 = PasswordField('Повторите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Регистрация')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Имя занято. Пожалуйста, используйте другое')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Такая почта уже используется')


class PostForm(FlaskForm):
    post = TextAreaField('Введите заметку', validators=[DataRequired(), Length(min=1, max=200)])
    submit = SubmitField('Подтвердить')


class EditForm(FlaskForm):
    post_field = TextAreaField('Редактировать', validators=[Length(min=1, max=200)])
    submit = SubmitField('Подтвердить')


class DeleteForm(FlaskForm):
    submit = SubmitField('Подтвердить')


class SearchForm(FlaskForm):
    search_field = TextAreaField('Искать', validators=[DataRequired()])
    submit = SubmitField('Найти')


