from wtforms import Form,StringField,IntegerField,PasswordField
from wtforms.validators import Length, NumberRange, DataRequired, Email, ValidationError,EqualTo
from app.models.user import User

class RegisterForm(Form):
    email = StringField(validators=[DataRequired(message='户名为空，请重新输入'),Length(min=8,max=64),Email(message='电子邮箱不符合规范')])
    password = PasswordField(validators=[DataRequired(message='密码不可为空，请输入密码'),Length(6,32)])
    nickname = StringField(validators=[DataRequired(),Length(2,16,message='昵称应为 2 到 16 个字符')])


    def validate_email(self,field):
        if User.query.filter_by(email = field.data).first():
            raise ValidationError('电子邮件已注册')

    def validate_nickname(self,field):
        if User.query.filter_by(nickname = field.data).first():
            raise ValidationError('此户名已被占用')


class LoginForm(Form):
    email = StringField(validators=[DataRequired(message='户名为空，请重新输入'),Length(min=8,max=64),Email(message='电子邮箱不符合规范')])
    password = PasswordField(validators=[DataRequired(message='密码不可为空，请输入密码'),Length(6,32)])

class EmailForm(Form):
    email = StringField(validators=[DataRequired(message='户名为空，请重新输入'),Length(min=8,max=64),Email(message='电子邮箱不符合规范')])

class ResetPasswordForm(Form):
    password1 = PasswordField(validators=[DataRequired(),Length(6,32,message='密码长度 为6~32字符之间，请输入密码'),EqualTo('password2',message='两次输入密码不相同')])
    password2 = PasswordField(validators=[DataRequired(),Length(6,32)])

class ChangePasswordForm(Form):
    old_password = PasswordField(validators=[DataRequired(message='密码不可为空，请输入密码'),Length(6,32)])
    new_password1 = PasswordField(validators=[DataRequired(), Length(6, 32, message='新密码长度 为6~32字符之间，请输入密码'),EqualTo('new_password2', message='两次输入密码不相同')])
    new_password2 = PasswordField(validators=[DataRequired(), Length(6, 32)])


