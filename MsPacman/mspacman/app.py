# -*- coding: utf-8 -*-
# dydrmntion@gmail.com ~ 2013

import os
import sys
import StringIO

from flask import (Flask, render_template, send_file, request, redirect,
                  url_for, Response)

from werkzeug.datastructures import Headers

_here = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(_here, 'mspacman'))

import mspacman


app = Flask(__name__)

app.mspacman = {}


@app.route('/')
def redirect_index():
    return redirect(url_for('.index'))


@app.route('/index', methods=['GET'])
def index():
    data = mspacman.get(request.args)
    return render_template('index.html', data=data)


@app.route('/package/<package>')
def package_audit(package):
    data = mspacman.audit(package)
    return render_template('package.html', data=data)


@app.route('/download-textfile', methods=['GET'])
def download_textfile():
  response = Response()
  response.status_code = 200

  f = StringIO.StringIO()
  f.write('\n'.join(request.args['packages'].split(',')))

  response.data = f.getvalue()

  response.headers = Headers({
    'Pragma': 'public',
    'Expires': '0',
    'Cache-Control': 'must-revalidate, pre-check=0, post-check=0',
    'Cache-Control': 'private',
    'Content-Type': 'text/plain',
    'Content-Disposition': 'attachement; filename=\"packages.txt\";',
    'Content-Transfer-Encoding': 'Binary',
    'Content-Length': len(response.data)
    })

  return response


def pacman_cmd():
    cmd = "sudo pacman -Rdc {}".format(" ".join(k for k, v in request.args.items()))

    app.mspacman['output_file'].write(cmd)

    mspacman.load_packages()

    return jsonify({'status': 'OK'})


@app.route('/assets/<path:filename>')
def assets(filename):
    sfile = os.path.join(_here, 'assets', filename)
    return send_file(sfile)


def start_app(host, port, output_file):

    app.mspacman['output_file'] = output_file

    app.run(host=host, port=port, debug=True)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
