from app.forms.auth import RegisterForm,LoginForm,EmailForm,ResetPasswordForm,ChangePasswordForm
from app.models.user import User
from app.models.base import db
from . import web
from flask import render_template, request, redirect, url_for,flash
from flask_login import login_user, logout_user, login_required
from app.libs.email_sender import send_email



    
    
@web.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method =='POST' and form.validate():
        with db.auto_commit():
            user = User()
            user.set_attrs(form.data)
            db.session.add(user)
        return redirect(url_for('web.login'))
    return render_template('auth/register.html',form=form)

@web.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user,remember=True)
            next = request.args.get('next')
            if not next or not next.startswith('/'):
                next = url_for('web.index')
            return redirect(next)
        else:
            flash('你未注册,或密码错误')
    return  render_template('auth/login.html',form=form)


@web.route('/reset/password', methods=['GET', 'POST'])
def forget_password_request():
    form = EmailForm(request.form)
    if request.method == 'POST':
        form = EmailForm(request.form)
        if form.validate():
            account_email = form.email.data
            #user =User.query.filter_by(email=account_email).first_or_404()
            user = User.query.filter_by(email=account_email).first()
            if user :
                send_email(form.email.data,'重置你的密码','email/reset_password.html',user=user,token = user.generate_token())
                flash('一封邮件已发送到邮箱'+account_email+'.请及时查收')
                return redirect(url_for('web.login'))
            else:
                flash('此邮箱未注册')
    return render_template('auth/forget_password_request.html',form=form)


@web.route('/reset/password/<token>', methods=['GET', 'POST'])
def forget_password(token):
    form =  ResetPasswordForm(request.form)
    if request.method == 'POST' and form.validate():
        success = User.change_password(token,form.password1.data)
        if success :
            flash('密码更新成功，请是用新密码登陆')
            return redirect(url_for('web.login'))
        else:
            flash('密码重置失败')
    return render_template('auth/forget_password.html',form=form)


@web.route('/change/password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm(request.form)
    if request.method == 'POST'and form.validate() :
        if current_user.check_password(form.old_password.data):
            success = User.change_password(0,form.new_password1.data,current_user.id)
            if success:
                flash('密码更新成功，请是用新密码登陆')
                return redirect(url_for('web.login'))
            else:
                flash('密码重置失败')
        flash('密码验证失败')
    return render_template('auth/change_password.html',form=form)


@web.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('web.index'))
