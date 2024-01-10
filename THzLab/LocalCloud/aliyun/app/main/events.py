from flask import session
from flask_socketio import emit, join_room, leave_room
from flask_redis import FlaskRedis
from .. import socketio

ROOM = 1

MASTER_STATUS = 0
SLAVE_STATUS = 0

MASSAGE_FROM_MASTER = []
MASSAGE_FROM_SLAVE = []

@socketio.on('joined', namespace='/chat')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    # room = session.get('room')
    join_room(ROOM)
    name = session.get('name')
    if name == 'master':
        MASTER_STATUS = 1
        emit('log', {'msg': '[LOG]:' + session.get('name') + ' has entered the room.'}, room=ROOM)
    elif name == 'slave':
        SLAVE_STATUS = 1
        emit('log', {'msg': '[LOG]:' + session.get('name') + ' has entered the room.'}, room=ROOM)
    if MASTER_STATUS and SLAVE_STATUS:
        emit('log', {'msg': '[LOG]:' + 'Ready to Start.'}, room=ROOM)
        emit('start', {'msg': 'start'}, room=ROOM)


@socketio.on('text', namespace='/chat')
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    # room = session.get('room')
    emit('message', {'msg': session.get('name') + ':' + message['msg']}, room=ROOM)


@socketio.on('left', namespace='/chat')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    # room = session.get('room')
    leave_room(ROOM)
    name = session.get('name')
    if name == 'master':
        MASTER_STATUS = 0
        emit('log', {'msg': '[LOG]:' + session.get('name') + ' has entered the room.'}, room=ROOM)
    elif name == 'slave':
        SLAVE_STATUS = 0
        emit('log', {'msg': '[LOG]:' + session.get('name') + ' has entered the room.'}, room=ROOM)

    emit('stop', {'msg': session.get('name') + ' has left the room.'}, room=ROOM)

