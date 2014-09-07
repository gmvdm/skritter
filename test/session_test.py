# -*- coding: utf-8 -*-

from skritter.session import session, Session
from skritter.exceptions import ConnectionError

import mock
import unittest


class TestSession(unittest.TestCase):
    def test_create_session(self):
        test_session = Session('client', 'client_secret')

        self.assertTrue(test_session.has_oauth_details())

    def test_create_empty_session(self):
        test_session = Session()
        self.assertFalse(test_session.has_oauth_details())

    def test_login_empty_session(self):
        test_session = Session()
        self.assertRaises(ConnectionError, test_session.login, 'user', 'secret')

    def test_login(self):
        mock_response = mock.Mock()
        mock_response.json.return_value = {'access_token': 'abc123'}

        mock_session = mock.Mock()
        mock_session.get.return_value = mock_response

        test_session = Session('client', 'client_secret', mock_session)
        test_session.login('user', 'user_secret')

        mock_session.get.assert_called_once()
        mock_session.headers.update.assert_called_once_with({'Authorization': 'Bearer abc123'})


class TestSessionVerbs(unittest.TestCase):
    def setUp(self):
        self.mock_response = mock.Mock()
        self.mock_session = mock.Mock()

        self.session = Session('client', 'client_secret', self.mock_session)

    def test_get(self):
        self.mock_response.status_code = 200
        self.mock_session.get.return_value = self.mock_response

        self.session.get('/test_url')

        self.mock_session.get.assert_called_once_with('/test_url')
        self.mock_response.json.assert_called_once_with()

    def test_post_json(self):
        test_data = {'key': 123}
        self.mock_session.post.return_value = self.mock_response

        self.session.post_json('/new', test_data)

        self.mock_session.post.assert_called_once_with('/new', '{"key": 123}')
        self.mock_response.json.assert_called_once_with()

    def test_put_json(self):
        test_data = {'key': 456}
        self.mock_session.put.return_value = self.mock_response

        self.session.put_json('/update', test_data)

        self.mock_session.put.assert_called_once_with('/update', '{"key": 456}')
        self.mock_response.json.assert_called_once_with()


class TestSessionFunction(unittest.TestCase):
    def test_session(self):
        test_session = session('client', 'secret')
        self.assertTrue(isinstance(test_session, Session))
        self.assertEqual(test_session.oauth_client_name, 'client')

    def test_session_requires_args(self):
        self.assertRaises(TypeError, session)


if __name__ == '__main__':
    unittest.main()
