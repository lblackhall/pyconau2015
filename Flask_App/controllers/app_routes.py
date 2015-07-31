__author__ = 'lachlan'

import logging

logger = logging.getLogger(__name__)

from flask import abort, request, render_template, g
from Flask_App import app, db_session
from Flask_App.models.services.user_service import UserService
from Flask_App.models.services.todo_service import TodoService
from Flask_App.controllers.forms import TodoForm, DeleteForm
from flask.ext.login import user_logged_in
from flask.ext.stormpath import login_required, user

from Flask_App.controllers.notifications import Notifications
from Flask_App.settings import FRIENDLY_SERVER_ERROR


@app.before_request
def before_request():
    g.notifications = Notifications()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/todo/')
@login_required
def todo_list():
    todo_service = TodoService(db_session)
    try:
        local_user = get_local_user(user)
        todos = todo_service.get_many_with_permission(local_user)
        if todos is None:
            todos = []
    except Exception as e:
        logger.error('Unable to retrieve actions from database with with error: {0}'.format(e))
        g.notifications.add_error(FRIENDLY_SERVER_ERROR)
    return render_template('list.html', todos=todos)


@app.route('/todo/add', methods=['GET', 'POST'])
@login_required
def person_add():
    btn_label = 'Create'
    hide_form = False
    form = TodoForm()

    if form.validate_on_submit():
        todo_service = TodoService(db_session)
        local_user = get_local_user(user)

        record = {}
        record['todo'] = form.data['todo']
        record['description'] = form.data['description']
        record['author'] = local_user

        try:
            todo_service.create(**record)
        except Exception as e:
            logger.error('Unable to create record: {0} with error: {1}'.format(record, e))
        else:
            g.notifications.add_success(u'Todo: {0} successfully added.'.format(
                record['todo']))
            hide_form = True

    else:
        g.notifications.add_wtf_errors(form)

    return render_template('add_edit.html', form=form, btn_label=btn_label, hide_form=hide_form)


@app.route('/todo/<id>/edit/', methods=['GET', 'POST'])
@login_required
def person_edit(id):
    btn_label = 'Update'
    hide_form = False
    form = TodoForm()
    todo_service = TodoService(db_session)
    local_user = get_local_user(user)
    if not todo_service.has_permission_from_id(id, local_user):
        return abort(403)

    if request.method == 'GET':
        record = todo_service.get_one(id)
        if record is not None:
            form.process(obj=record)
        else:
            abort(404)

    if form.validate_on_submit():
        record = {}
        record['todo'] = form.data['todo']
        record['description'] = form.data['description']
        id = form.data['id']

        try:
            todo_service.update(id, **record)
        except Exception as e:
            logger.error('Unable to update record: {0} with error: {1}'.format(record, e))
        else:
            g.notifications.add_success(u'ToDo: {0} successfully updated.'.format(
                record['todo']))
            hide_form = True

    else:
        g.notifications.add_wtf_errors(form)

    return render_template('add_edit.html', form=form, btn_label=btn_label, hide_form=hide_form)


@app.route('/todo/<id>/delete/', methods=['GET', 'POST'])
@login_required
def todo_delete(id):
    hide_form = False
    msg = u''
    form = DeleteForm()
    todo_service = TodoService(db_session)
    local_user = get_local_user(user)
    if not todo_service.has_permission_from_id(id, local_user):
        return abort(403)

    if request.method == 'GET':
        record = todo_service.get_one(id)
        if record is not None:
            form.process(obj=record)
            msg = u'Are you sure you want to delete the ToDo: {0}?'.format(
                record.todo)
        else:
            abort(404)

    if form.validate_on_submit():
        id = form.data['id']
        try:
            todo_service.delete(id)
        except Exception as e:
            logger.error('Unable to delete record with error: {1}'.format(e))
        else:
            g.notifications.add_success(u'ToDo successfully deleted.')
            hide_form = True

    return render_template('delete.html', form=form, msg=msg, hide_form=hide_form)


# Methods related to users and login
@user_logged_in.connect_via(app)
def on_user_logged_in(sender, user):
    user_service = UserService(db_session)
    local_user = user_service.get_by_remote_id(user.href)
    if local_user is None:
        local_user = user_service.create(**{'remote_id': user.href})


def get_local_user(user):
    user_service = UserService(db_session)
    local_user = user_service.get_by_remote_id(user.href)
    return local_user
