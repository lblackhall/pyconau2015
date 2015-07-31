__author__ = 'lachlan'

import logging


class ServiceLayerError(Exception):
    pass


class DataService(object):
    def __init__(self, db_session):
        self.db = db_session
        self.tablename = None
        self.logger = logging.getLogger(__name__)

    def create(self, **fields):
        try:
            record = self.tablename(**fields)
            self.db.add(record)
            self.db.commit()
            return self.get_one(record.id)
        except Exception as e:
            self.logger.error("Error occurred while creating record with error msg: %s" % (str(e)))
            self.db.rollback()
            raise ServiceLayerError("Error occurred while creating record with error msg: %s" % (str(e)))

    def update(self, id, **fields):
        if self.exists(id):
            try:
                self.db.query(self.tablename).filter(self.tablename.id == id).update(fields)
                record = self.get_one(id)
                self.db.add(record)
                self.db.commit()
                return self.get_one(record.id)
            except Exception as e:
                self.logger.error("Error occurred while updating record with error msg: %s" % (str(e)))
                self.db.rollback()
                raise ServiceLayerError("Error occurred while updating record with error msg: %s" % (str(e)))
        else:
            raise ServiceLayerError()

    def get_one(self, id):
        try:
            if self.exists(id):
                return self.db.query(self.tablename).get(id)
            else:
                return None
        except Exception as e:
            self.logger.error("Error occurred while retrieving individual record with error msg: %s" % (str(e)))
            self.db.rollback()
            raise ServiceLayerError("Error occurred while retrieving individual record with error msg: %s" % (str(e)))

    def get_many(self):
        try:
            req = self.db.query(self.tablename).all()
            if req == []:
                return None
            else:
                return req
        except Exception as e:
            self.logger.error("Error occurred while retrieving multiple records with error msg: %s" % (str(e)))
            self.db.rollback()
            raise ServiceLayerError("Error occurred while retrieving multiple records with error msg: %s" % (str(e)))

    def delete(self, id):
        try:
            if self.exists(id):
                record = self.get_one(id)
                self.db.delete(record)
                self.db.commit()
                return record
            else:
                return None
        except Exception as e:
            self.logger.error("Error occurred while deleting record with error msg: %s" % (str(e)))
            self.db.rollback()
            raise ServiceLayerError("Error occurred while deleting record with error msg: %s" % (str(e)))

    def exists(self, id):
        if self.db.query(self.tablename).get(id) == None:
            return False
        else:
            return True

    def get_many_with_permission(self, user):
        try:
            req = self.db.query(self.tablename).filter(getattr(self.tablename, 'author') == user).all()
            if req == []:
                return None
            else:
                return req
        except Exception as e:
            self.logger.error("Error occurred while retrieving multiple records with error msg: %s" % (str(e)))
            self.db.rollback()
            raise ServiceLayerError("Error occurred while retrieving multiple records with error msg: %s" % (str(e)))

    def has_permission_from_id(self, id, user):
        req = self.db.query(self.tablename).filter(self.tablename.id == id).first()
        if req == []:
            return False
        else:
            if req.author == user:
                return True
            else:
                return False
