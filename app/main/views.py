from flask import render_template, request
from . import main
from .. import db
from ..models import Message
import json
import re

@main.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@main.route('/messages', methods=['GET'])
def get_messages():
    result = dict()
    code = None

    messages = Message.query.all()
    if len(messages) > 0:
        message_results = list()
        for message in messages:
            if is_base64(message.content):
                message_to_add = {'id': message.id, 'content': message.content }
                message_results.append(message_to_add)
        result.update({ 'messages': message_results })
        result.update({ 'success': True })
        code = 200
    else:
        result.update({ 'success': False })
        result.update({ 'message': 'not found' })
        code = 404
    return json.dumps(result), code
   
@main.route('/messages', methods=['POST'])
def add_message():
    result = dict()
    code = None

    content = request.form['content']
    if content is None:
        result.update({ 'success': False })
        result.update({ 'message': 'missing content' })
        code = 500
    elif is_base64(content) is False:
        result.update({ 'success': False })
        result.update({ 'message': 'content is not base64 encoded' })
        code = 500
    else:
        message = Message(content=request.form['content'])
        db.session.add(message)
        result.update({ 'success': True })
        code = 200
    return json.dumps(result), code

def is_base64(string):
    if len(string) % 4 == 0 and re.match('^[A-Za-z0-9+\/=]+\Z', string):
        return(True)
    else:
        return(False)
