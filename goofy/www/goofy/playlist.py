# -*- coding: utf-8 -*-
# dydrmntion@gmail.com ~ 2013

import re
import logging
import time
import urllib
import json

import requests
from BeautifulSoup import BeautifulSoup

from goofy import constants, utils


logger = logging.getLogger(__name__)


class Playlist(object):

    tracks = []

    last_api_req = 0

    def __init__(self, name, api_url, play_url=None, playlist_url=None,
                 tracks=None):
        '''Either loads meta data using the supplied provider playlist url or
        uses the meta data retrieved by the other provider to build a playlist

        '''

        self.name = name

        self.api_url = api_url

        self.play_url = play_url

        self.cache = utils.ApiCache(self.name)

        self.error = False

        if playlist_url:

            self.playlist_url = playlist_url

            self.tracks = self.load(self.playlist_url)

        elif tracks:

            self.tracks, self.track_ids = self.create(tracks)

        else:

            raise GoofyPlaylistError('Should not happen.')

    def create(self, tracks):
        '''Retrieves track ids for the current provider'''

        _tracks = []

        track_ids = []

        for track in tracks:

            track_id = self._get_track_id(track)

            if track_id:

                _tracks.append(track)

                track_ids.append(track_id)

        return _tracks, track_ids

    def load(self, url):
        '''Retrieves track meta data for the playlist'''

        self.playlist_url = url

        tracks = []

        try:

            for artist, title in self._load_url(url):

                tracks.append({
                    'artist': urllib.unquote(artist),
                    'title': urllib.unquote(title),
                })

        except AttributeError:

            pass

        else:

            if tracks:

                return tracks

        raise GoofyPlaylistError('invalid playlist url'.format(url), 'FORM')

    def _api_req(self, resource, params={}, request_method='GET'):
        '''The api wrapper for the current provider'''

        if time.time() - self.last_api_req < 1.0 / 20:

            logger.debug('{0} -> zZz.'.format(self.name))

            time.sleep(1.0 / 20)

        url = '{0}/{1}'.format(self.api_url, resource)

        headers = {'User-Agent': constants.USER_AGENT}

        req = requests.Request(request_method, url, params=params,
                               headers=headers).prepare()

        logger.info('Prepared {0!r} api request: {1!r}.'.format(self.name,
                                                                req.url))

        resp = self.cache.from_cache(req)

        if resp:
            # Found a cached response.
            status_code = 200

        else:

            session = requests.session()

            resp = session.send(req)

            self.cache.to_cache(resp)

            self.last_api_req = time.time()

            status_code = resp.status_code

            resp = resp.content

        if not status_code in (200, 302, 502):

            raise GoofyPlaylistError(
                'Error while making request: {0!r} / {1!r}.'.format(
                    resp.url, status_code))

        if status_code == 502:

            return self._api_call(resource, params)

        try:

            resp = json.loads(resp)

        except ValueError:

            logger.warning('Error! Could  not deserialize api response.')

        else:

            return resp

    def get_resolved_track_ids(self):

        return ','.join(self.track_ids)


class SpotifyPlaylist(Playlist):

    def __init__(self, playlist_url=None, tracks=None):

        Playlist.__init__(self, name='spotify',
                          api_url='http://ws.spotify.com',
                          play_url="https://embed.spotify.com/?url={url}",
                          playlist_url=playlist_url,
                          tracks=tracks)

    def _load_url(self, url):

        req = requests.get(self.play_url.format(**vars()))

        soup = BeautifulSoup(req.content)

        for track in soup.findAll('ul', {'class': 'track-info'}):

            yield [
                track.find('li', {'class': re.compile(r'artist')}).text,
                track.find('li', {'class': re.compile(
                    r'track-title')}).text.split('. ')[-1]
            ]

    def _get_track_id(self, track):

        resource = 'search/1/track.json?'

        params = {'q': ' '.join(track.values()).lower()}

        api_resp = self._api_req(resource=resource, params=params)

        try:

            return api_resp['tracks'][0]['href'].split(':')[-1]

        except IndexError:
            # Api returned an empty result set.
            pass


class DeezerPlaylist(Playlist):

    def __init__(self, playlist_url=None, tracks=None):

        Playlist.__init__(self, name='deezer',
                          api_url='https://api.deezer.com/2.0',
                          playlist_url=playlist_url,
                          tracks=tracks)

    def _load_url(self, url):

        resource = 'playlist/' + url.split('/')[-1]

        api_resp = self._api_req(resource)

        if isinstance(api_resp, int):

            return

        for track in api_resp.get('tracks').get('data'):

            yield [
                track.get('artist').get('name'),
                track.get('title')
            ]

    def _get_track_id(self, track):

        resource = 'search?'

        params = {
            'q': ' '.join(track.values()).lower()
        }

        api_resp = self._api_req(resource, params)

        if not isinstance(api_resp, int):

            try:

                return api_resp['data'][0]['id']

            except (KeyError, IndexError):

                logger.warning('Could not find track id for: {0!r}.'.format(
                    ' - '.join(track.values())))

    def create_playlist(self, access_token):

        # Get user id
        resource = 'user/me?'

        params = {'access_token': access_token}

        api_resp = self._api_req(resource, params)

        user_id = api_resp.get('id')

        # Create new playlist
        resource = 'user/{0}/playlists'.format(user_id)

        unique_id = str(int(time.time()))[-5:]

        params = {
            'title': 'GoofyPlaylist-{0}'.format(unique_id),
            'access_token': access_token
        }

        api_resp = self._api_req(resource, params, 'POST')

        playlist_id = api_resp.get('id')

        resource = 'playlist/{0}/tracks'.format(playlist_id)

        params = {
            'access_token': access_token,
            'songs': ','.join(str(x) for x in self.track_ids)
        }

        self._api_req(resource, params, 'POST')


def get_playlists(url, provider):

    providers = [SpotifyPlaylist, DeezerPlaylist]

    if provider != 'spotify':

        providers.reverse()

    playlistA = providers.pop(0)(playlist_url=url)

    playlistB = providers.pop()(tracks=playlistA.tracks)

    return playlistA, playlistB


class GoofyPlaylistError(Exception):

    pass
