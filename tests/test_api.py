import unittest
from flask import url_for
from server import create_app, db
from server.models import Server


class BasicsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        s = Server('192.168.1.1', 'Some Dev Server', True)

        db.session.add(s)
        db.session.commit()

        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_server_update(self):
        # test invalid server id
        req = self.client.post(url_for('api.update_server_information', server_id='5'), data={'map': 'surf_test'})
        self.assertTrue(req.status_code == 400)

        # test valid server id
        req = self.client.post(url_for('api.update_server_information', server_id='1'), data={'map': 'surf_test'})
        self.assertTrue(req.status_code == 200)

        # test invalid map data
        req = self.client.post(url_for('api.update_server_information', server_id='1'))
        self.assertTrue(req.status_code == 400)
