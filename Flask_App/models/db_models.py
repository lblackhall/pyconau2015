__author__ = 'lachlan'

from Flask_App import db
from sqlalchemy.ext.declarative import declared_attr

# Create mapping from db objects to named objects for simplicity
Model = db.Model
Column = db.Column
String = db.String
Integer = db.Integer
DateTime = db.DateTime
ForeignKey = db.ForeignKey
relationship = db.relationship
Boolean = db.Boolean
Text = db.Text


class Users(Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    remote_id = Column(String)
    email = Column(String)

    def __repr__(self):
        return '<User>: {0}'.format(self.email)


class HasAuthor(object):
    @declared_attr
    def author_id(cls):
        return Column(Integer, ForeignKey('users.id'))

    @declared_attr
    def author(cls):
        return relationship('Users')


class Todo(Model, HasAuthor):
    __tablename__ = 'experiences'

    id = Column(Integer, primary_key=True, index=True)
    todo = Column(String)
    description = Column(Text)

    def __repr__(self):
        return '<User>: {0}'.format(self.description)
