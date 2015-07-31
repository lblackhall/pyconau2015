__author__ = 'Lachlan'

from Flask_App.models.services.data_service import DataService, ServiceLayerError
from Flask_App.models.db_models import Users

class UserService(DataService):

    def __init__(self, db):
        super(UserService, self).__init__(db)
        self.tablename = Users

    def get_by_remote_id(self, remote_id):
        try:
            req = self.db.query(self.tablename).filter(getattr(self.tablename, 'remote_id') == remote_id).first()
            if req is None:
                return None
            else:
                return req
        except Exception as e:
            self.logger.error("Error occurred while retrieving individual record by name: {0} with error msg: {1}".format(remote_id, e))
            self.db.rollback()
            raise ServiceLayerError("Error occurred while retrieving individual record by name: {0} with error msg: {1}".format(remote_id, e))