from threading import Thread
from app import mail
from flask_mail import Message
from flask import current_app,render_template


def send_async_email(app,msg):
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            pass

def send_email(to,subject,template,**kwargs):
    #msg = Message('测试邮件',sender = 'kingnlionheart@163.com',body='Test',recipients= ['user@qq.com'])
    msg = Message('[平凡之路]'+' '+subject ,sender=current_app.config['MAIL_USERNAME']+'@163.com',recipients=[to])
    msg.html = render_template(template,**kwargs)

    app = current_app._get_current_object()
    thr = Thread(target=send_async_email,args=[app,msg])
    thr.start()

    #mail.send(msg)
