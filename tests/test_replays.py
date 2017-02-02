import unittest
from flask import url_for
from server import create_app, db
from server.models import Replay


class BasicsTestCase(unittest.TestCase):
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

    def test_list_replays(self):
        # test empty database
        req = self.client.get(url_for('replays.list_replays'))
        self.assertTrue(req.status_code == 200)
