from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy
from flask_sqlalchemy import  BaseQuery
from sqlalchemy import Column,SmallInteger,Integer
from contextlib import contextmanager
from datetime import datetime



class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e


class Query(BaseQuery):
    def filter_by(self, **kwargs):
        kwargs['status'] = 1
        return super(Query,self).filter_by(**kwargs)


db = SQLAlchemy(query_class=Query)

class Base(db.Model):
    __abstract__ =True
    status = Column(SmallInteger,default=1)
    create_time = Column('create_time',Integer)


    def __init__(self):
        self.create_time = int(datetime.now().timestamp())

    def set_attrs(self,attrs_dict):
        for key,value in attrs_dict.items():
            if key != id and hasattr(self,key):
                setattr(self,key,value)
    @property
    def create_datetime(self):
        if self.create_time:
            return datetime.fromtimestamp(self.create_time)
        else:
            return None
    def delete(self):
        self.status = 0
