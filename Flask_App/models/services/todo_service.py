__author__ = 'Lachlan'

from Flask_App.models.services.data_service import DataService
from Flask_App.models.db_models import Todo

class TodoService(DataService):

    def __init__(self, db):
        super(TodoService, self).__init__(db)
        self.tablename = Todo
