__author__ = 'Lachlan'

from flask.ext.wtf import Form
from wtforms import StringField, HiddenField

class TodoForm(Form):
    todo = StringField('ToDo')
    description = StringField('Description')
    id = HiddenField(default='')

class DeleteForm(Form):
    id = HiddenField(default='')
