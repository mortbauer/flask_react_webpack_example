#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import eventlet
eventlet.monkey_patch()

import os
import time
import json

import logging
import coloredlogs
from datetime import datetime
import threading

from flask import Flask, render_template
from flask import send_from_directory
from flask.ext.socketio import SocketIO, emit


logger = logging.getLogger('flask-app')

web = Flask(__name__)
web.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(web,async_mode='eventlet')

def producer():
    while True:
        time.sleep(5)
        logger.info('sending periodic')
        socketio.emit('ready', {'ready': datetime.utcnow().strftime('%B %d, %Y %S')})

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
    if int(data.get('connection_attempt', 0)) == 0:
        emit('zeromq', 'Hey, this is a message coming from flask through socket.io\n')
    else:
        emit('zeromq', 'reconnected to server\n')
    for i in range(5):
        emit('ready', {'ready': datetime.utcnow().strftime('%B %d, %Y %S')})


@socketio.on('zeromq')
def websocket_zeromq(*args, **kwargs):
    logger.info('entered zeromq')


if __name__ == '__main__':
    coloredlogs.install(level=logging.DEBUG, show_hostname=False)
    t = threading.Thread(target=producer)
    t.daemon = True
    t.start()
    socketio.run(web, host='0.0.0.0',debug=True,use_reloader=True)
