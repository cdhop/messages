import unittest
from flask import url_for
from app import create_app, db
from app.models import Message

class FlaskClientTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_index_page(self):
        response = self.client.get(url_for('main.index'))
        self.assertEqual(response.status_code, 200)

    def test_good_post_message(self):
        response = self.client.post(url_for('main.add_message'), \
            data = { 'content': 'VGhpcyBpcyBhIHRlc3QK' })
        self.assertTrue(response.status_code, 200)

    def test_bad_post_message(self):
        response = self.client.post(url_for('main.add_message'), \
            data = { 'content': 'This is a test' })
        self.assertTrue(response.status_code, 500) 

    def test_get_messages(self):
        # post a good message
        post_response = self.client.post(url_for('main.add_message'), \
            data = { 'content': 'VGhpcyBpcyBhIHRlc3QK' })

        # post a bad message
        post_response2 = self.client.post(url_for('main.add_message'), \
            data = { 'content': 'This is a test' })

        get_response = self.client.get(url_for('main.get_messages'))

        self.assertTrue(get_response.status_code, 200)
        self.assertTrue('VGhpcyBpcyBhIHRlc3QK' in str(get_response.data)) 
        self.assertFalse('This is a test' in str(get_response.data))
