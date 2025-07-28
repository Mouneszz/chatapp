from flask import request
from . import socketio
from flask_socketio import emit

@socketio.on('send_message')
def handle_send_message(data):
    emit('receive_message', {
        'message': data['message'],
        'sender_id': request.sid  # Unique ID for the sender's socket
    }, broadcast=True)
