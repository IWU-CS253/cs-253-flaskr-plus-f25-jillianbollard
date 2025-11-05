import os
import app as flaskr
import unittest
import tempfile

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
        flaskr.app.testing = True
        self.app = flaskr.app.test_client()
        with flaskr.app.app_context():
            flaskr.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(flaskr.app.config['DATABASE'])

    def test_empty_db(self):
        rv = self.app.get('/')
        assert b'No entries here so far' in rv.data

    def test_messages(self):
        rv = self.app.post('/add', data=dict(
            title='<Hello>',
            text='<strong>HTML</strong> allowed here',
            category='A category'
        ), follow_redirects=True)
        assert b'No entries here so far' not in rv.data
        assert b'&lt;Hello&gt;' in rv.data
        assert b'<strong>HTML</strong> allowed here' in rv.data
        assert b'A category' in rv.data

    def test_message_editing(self):
        # ask professor sheese if you can call the test_messages() function within this test
        self.app.post('/add', data={
            'title': 'Original Title',
            'category': 'Original Category',
            'text': 'Original Text'
        }, follow_redirects=True)

        with self.app.application.app_context():
            db = self.db_fd
            post = db.execute('SELECT id FROM entries WHERE title = ?', ('Original Title',)).fetchone()
            post_id = post['id']

        response = self.app.post(f'/edit/{post_id}', data={
            'title': 'New Title',
            'category': 'New Category',
            'text': 'New Text'
        }, follow_redirects=True)

        assert b'New Title' in response.data
        assert b'New Category' in response.data
        assert b'New Text' in response.data


if __name__ == '__main__':
    unittest.main()