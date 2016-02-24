#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import json
import gevent
import gevent.monkey
gevent.monkey.patch_all()

import zmq.green as zmq
from subprocess import Popen, PIPE, STDOUT
import logging
import coloredlogs
from datetime import datetime

from flask import Flask, render_template
from flask import send_from_directory
from flask.ext.socketio import SocketIO, emit

logger = logging.getLogger('flask-app')

web = Flask(__name__)
web.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(web)

zmq_context = zmq.Context()


@web.route('/', defaults={'path': ''})
@web.route('/<path:path>')
def index(path):
    return render_template('index.html')


@web.route('/favicon.ico')
def favicon():
    return send_from_directory('styles', 'favicon.ico')


@web.route('/dist/<path:path>')
def send_js(path):
    return send_from_directory('dist', path)


@socketio.on('hello')
def websocket_hello(data):
    logger.info('client connected %s: ', data)
    emit('ready', {'ready': datetime.utcnow().strftime('%B %d, %Y')})
    gevent.sleep(0)
    if int(data.get('connection_attempt', 0)) == 0:
        emit('zeromq', b'Hey, this is a message coming from flask through socket.io\n')
    else:
        emit('zeromq', b'reconnected to server\n')


@socketio.on('zeromq')
def websocket_zeromq(*args, **kwargs):
    logger.info('entered zeromq')


if __name__ == '__main__':
    coloredlogs.install(level=logging.DEBUG, show_hostname=False)
    socketio.run(web, host='0.0.0.0')
