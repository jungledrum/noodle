from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker, relationship, backref
from globals import db

Base = declarative_base()

class ModelBase():

    @classmethod
    def all(cls):
        return db.query(cls)

    @classmethod
    def find(cls, id):
        return db.query(cls).get(id)

    @classmethod
    def where(cls, stmt):
        return db.query(cls).filter(stmt)

    def save(self):
        db.add(self)
        db.commit()

    def update(self, args):
        for (k,v) in args.items():
            setattr(self, k, v)
            db.add(self)
            db.commit()

    def destroy(self):
        db.delete(self)
        db.commit()

