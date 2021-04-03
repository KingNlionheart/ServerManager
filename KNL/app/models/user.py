from math import floor

from werkzeug.security import generate_password_hash,check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from .base import Base,db
from sqlalchemy import Column,Integer,String,Boolean,Float
from flask_login import UserMixin
from flask import current_app
from app import login_manager


class User(Base,UserMixin):
    id = Column(Integer,primary_key=True)
    nickname = Column(String(48),nullable=False)
    phone_number = Column(String(18),unique=True)
    _password = Column('password',String(128),nullable=False)
    email = Column(String(50),unique=True,nullable=False)
    confirmed = Column(Boolean,default=False)
    beans = Column(Float,default=0)
    send_counter = Column(Integer,default=0)
    receive_counter = Column(Integer,default=0)
    wx_open_id = Column(String(50))
    wx_name = Column(String(32))

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self,raw):
        self._password = generate_password_hash(raw)

    def check_password(self,raw):
        return  check_password_hash(self._password,raw)

    def generate_token(self,expiration=600):
        s = Serializer(current_app.config['SECRET_KEY'],expiration)
        return s.dumps({'id':self.id}).decode('utf-8')


    @staticmethod
    def change_password(token,new_password,uid=None):
        if uid :
            with db.auto_commit():
                user = User.query.get(uid)
                user.password = new_password
            return True
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        uid = data.get('id')
        with db.auto_commit():
            user = User.query.get(uid)          #是主键时候 可以用 get() 但也可以用平时的 filter_by()
            user.password = new_password
        return True

    @property
    def summary(self):
        return dict(
            nickname = self.nickname,
            beans = self.beans,
            email = self.email,
            send_receive = str(self.send_counter)+'/'+ str(self.receive_counter)
        )

@login_manager.user_loader
def get_user(uid):
    return User.query.get(int(uid))
