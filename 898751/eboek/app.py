# -*- coding: utf-8 -*-
# dydrmntion@gmail.com ~ 2013

from flask import (Flask, render_template, redirect, url_for, request,
                   Response)
from flask.ext.login import (login_required, logout_user, current_user)

from eboek import config, auth, helpers


app = Flask(__name__)

app.config.update(SECRET_KEY=config.SECRET_KEY)

auth.login_manager.setup_app(app)


@app.route("/login", methods=["GET", "POST"])
def login():

    warning = False

    if request.method == 'POST':

        username = request.form.get('username', 'null')

        password = request.form.get('password', 'null')

        if auth.validate_login(username, password, request.remote_addr):

            return redirect(url_for('.browse', page_num=1))

        else:

            warning = True

    return render_template('login.html', warning=warning)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return Response('<p>Logged out</p>')


@app.errorhandler(401)
def page_not_found(e):
    return Response('<p>Login failed</p>')


@app.route('/')
@login_required
def redirect_from_root():

    return redirect(url_for('.login'))


@app.route('/browse/page<page_num>')
@login_required
def browse(page_num):

    return render_template('browse.html',
                           helper=helpers.BrowseHelper(current_user,
                                                       int(page_num)))


@app.route('/search', methods=['POST', 'GET'])
@login_required
def search():

    query = request.form.get('query', False)

    return render_template('results.html',
                           helper=helpers.SearchHelper(query,
                                                       current_user))


@app.route('/booklist/modal', methods=['POST', 'GET'])
@login_required
def booklist_modal():

    book_id = request.args.get('id')

    h = helpers.ModalBookListHelper(current_user.id)

    h.set_modal(book_id)

    return render_template('booklist_modal.html',
                           helper=h, referrer=request.referrer)


@app.route('/booklist/update', methods=['POST', 'GET'])
@login_required
def booklist_update():

    h = helpers.ModalBookListHelper(current_user.id)

    if request.args.get('add'):

        h.append(request.args.get('add'))

    elif request.args.get('remove'):

        h.remove(request.args.get('remove'))

        if request.args.get('remove') == 'all':

            return redirect(url_for('.booklist'))

    return redirect(request.args.get('referrer'))


@app.route('/booklist')
@login_required
def booklist():

    h = helpers.BookListHelper(current_user)

    return render_template('booklist.html', helper=h)


if __name__ == '__main__':

    app.run(host='0.0.0.0', debug=True)
