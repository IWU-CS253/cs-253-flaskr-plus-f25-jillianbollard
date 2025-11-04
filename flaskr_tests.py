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












    def test_message_edit(self):
        # Step 1: Add a post to edit
        self.app.post('/add', data={
            'title': 'Original Title',
            'category': 'General',
            'text': 'Original content.'
        }, follow_redirects=True)

        # Step 2: Get the post ID (assuming it's the first post)
        with self.app.application.app_context():
            db = get_db()
            post = db.execute('SELECT id FROM entries WHERE title = ?', ('Original Title',)).fetchone()
            post_id = post['id']

        # Step 3: Edit the post
        response = self.app.post(f'/edit/{post_id}', data={
            'title': 'Updated Title',
            'category': 'Updated Category',
            'text': 'Updated content.'
        }, follow_redirects=True)

        # Step 4: Check that the updated content appears
        assert b'Updated Title' in response.data
        assert b'Updated Category' in response.data
        assert b'Updated content.' in response.data

        # Step 5: Ensure old content is gone
        assert b'Original Title' not in response.data
        assert b'Original content.' not in response.data

if __name__ == '__main__':
    unittest.main()