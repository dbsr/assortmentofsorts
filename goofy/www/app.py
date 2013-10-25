# -*- coding: utf-8 -*-
# dydrmntion@gmail.com ~ 2013

import logging
from datetime import datetime

from flask import (Flask, render_template, send_file, request, redirect,
                   url_for, jsonify, session)

from goofy import playlist, constants, deezer_oauth_client
import goofy


app = Flask(__name__)

app.secret_key = "HUSH"

app.providers = []

app.oauth_client = deezer_oauth_client.DeezerClient('manage_library',
                                                    **constants.DEEZER_OAUTH)

logger = logging.getLogger(goofy.name)


@app.route('/oauth', methods=['GET', 'POST'])
def oauth_login():

    if not request.args:

        token, expires = session.get('oauth_token', (None, None))

        if token and datetime.now() < expires:

            return redirect(url_for('.create_deezer_playlist'))

        if token:

            del session['oauth_token']

        return redirect(app.oauth_client.get_authorization_code_uri())

    elif request.args.get('code'):

        session['oauth_token'] = (
            token, expires) = app.oauth_client.get_token(
                request.args.get('code'))

        return redirect(url_for('.oauth_login'))


@app.route('/create-deezer-playlist')
def create_deezer_playlist():

    if not app.providers or app.providers[1].name != 'deezer':

        return redirect(url_for('.index'))

    elif not session.get('oauth_token'):

        logger.debug('no token found, redirecting to oauth')

        return redirect(url_for('.oauth'))

    try:

        app.providers[1].create_playlist(session.get('oauth_token')[0])

    except playlist.GoofyPlaylistError as e:

        logger.error(e.message)

        ok = False

    else:

        ok = True

    return jsonify(dict(ok=ok))


@app.route('/', methods=['GET', 'POST'])
def index():

    if request.args.get('direction'):

        provider = request.args.get('direction')

        playlist_url = request.args.get('playlist_url')

        logger.debug('Received stage 1 GET request: {0!r}, {1!r}.'.format(
            provider, playlist_url))

        try:

            app.providers = playlist.get_playlists(playlist_url, provider)

        except playlist.GoofyPlaylistError as e:

            if 'FORM' in e.args:

                return jsonify({
                    'status': 'INPUT_ERROR',
                    'message': e.args[0]
                })

            logger.error('ERROR! playlist processing: {0}, {1}'.format(
                provider, playlist_url))

            return redirect(url_for('.index'))

        else:

            return jsonify({
                'plugin_data': app.providers[1].get_resolved_track_ids(),
                'provider': app.providers[1].name
            })

    return render_template('index.html')



@app.route('/<directory>/<filename>')
def static(directory, filename):

    if directory == 'toaster':
        return send_file('js/toaster/{0}'.format(filename))

    return send_file('{0}/{1}'.format(directory, filename))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
