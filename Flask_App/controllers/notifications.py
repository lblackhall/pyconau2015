__author__ = 'Lachlan'

class Notifications(object):

    def __init__(self):
        self.errors = []
        self.warnings = []
        self.info = []
        self.success = []

    def add_error(self, msg):
        self.errors.append(msg)

    def add_warning(self, msg):
        self.warnings.append(msg)

    def add_info(self, msg):
        self.info.append(msg)

    def add_success(self, msg):
        self.success.append(msg)

    def add_wtf_errors(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                self.add_error(u"Error in the {0} field - {1}".format(getattr(form, field).label.text, error))
