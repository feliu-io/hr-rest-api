import json

from models.user import AppUserModel
from tests.base_test import BaseTest


class TestUser(BaseTest):
    """System tests for the user resource."""
    def setUp(self):
        """
        Extend the BaseTest setUp method by creating a dict
        representing another user.
        """
        super(TestUser, self).setUp()
        with self.app_context():
            self.other_u.is_owner = False
            self.other_u.save_to_db()

            self.u_dict = {
                'username': 'test_another_u',
                'password': 'test_p',
                'email': 'test_another_u@test_o.com',
                'organization_id': self.get_organization().id,
                'is_super': False,
                'is_owner': True,
                'is_active': True
            }

    def test_user_post_with_authentication(self):
        """
        Test that a POST request to the /user endpoint returns
        status code 201 and that the user is present in the
        database after the POST request.
        """
        with self.app() as c:
            with self.app_context():
                self.assertIsNone(AppUserModel.find_by_username(
                    self.u_dict['username']))

                r = c.post('/user',
                           data=json.dumps(self.u_dict),
                           headers=self.get_headers())

                user = json.loads(r.data)['user']

                self.assertEqual(r.status_code, 201)
                self.assertEqual(user['username'],
                                 self.u_dict['username'])
                self.assertEqual(user['email'],
                                 self.u_dict['email'])
                self.assertEqual(user['organization_id'],
                                 self.u_dict['organization_id'])
                self.assertFalse(user['is_super'])
                self.assertTrue(user['is_owner'])
                self.assertTrue(user['is_active'])
                self.assertIsNotNone(AppUserModel.find_by_username('test_u'))

    def test_user_post_without_authentication(self):
        """
        Test that a POST request to the /user endpoint returns
        status code 401 if the user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send POST request to the /user endpoint with
                # wrong authentication header.
                r = c.post('/user',
                           data=json.dumps(self.u_dict),
                           headers={
                               'Content-Type': 'application/json',
                               'Authorization': 'JWT FaKeToKeN!!'
                           })

                self.assertEqual(r.status_code, 401)

    def test_user_post_duplicate(self):
        """
        Test that status code 400 is returned when trying to
        POST duplicated data to the /user endpoint.
        """
        with self.app() as c:
            with self.app_context():
                c.post('/user',
                       data=json.dumps(self.u_dict),
                       headers=self.get_headers())

                r = c.post('/user',
                           data=json.dumps(self.u_dict),
                           headers=self.get_headers())

                self.assertEqual(r.status_code, 400)

    def test_user_post_wrong_user(self):
        """
        Test that status code 403 is returned when trying to POST a
        user with a user without permission.
        """
        with self.app() as c:
            with self.app_context():
                r = c.post('/user',
                           data=json.dumps(self.u_dict),
                           headers=self.get_headers({
                               'username': 'test_other_u',
                               'password': 'test_p'
                           }))

                self.assertEqual(r.status_code, 403)

    def test_user_get_with_authentication(self):
        """
        Test that a GET request to the /user/<string:username>
        endpoint returns the correct user if the user is
        authenticated.
        """
        with self.app() as c:
            with self.app_context():
                r = c.get(f'/user/{self.get_user(self.u_dict).username}',
                          headers=self.get_headers())

                user = json.loads(r.data)

                self.assertEqual(r.status_code, 200)
                self.assertEqual(user['username'],
                                 self.u_dict['username'])

    def test_user_get_not_found(self):
        """
        Test that a GET request to the /user/<string:username> endpoint
        returns status code 404 if the user is not found in the database table.
        """
        with self.app() as c:
            with self.app_context():
                r = c.get(f'/user/{self.u_dict["username"]}',
                          headers=self.get_headers())

                self.assertEqual(r.status_code, 404)

    def test_user_get_without_authentication(self):
        """
        Test that a GET request to the /user/<string:username> endpoint
        returns status code 401 if the user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send the GET request to the /user endpoint with
                # wrong authentication header.
                r = c.get(f'/user/{self.get_user(self.u_dict).username}',
                          headers={
                              'Content-Type': 'application/json',
                              'Authorization': 'JWT FaKeToKeN!!'
                          })

                self.assertEqual(r.status_code, 401)

    def test_user_put_with_authentication(self):
        """
        Test that a PUT request to the /user/<string:username>
        endpoint returns status code 200.
        """
        with self.app() as c:
            with self.app_context():
                r = c.put(f'/user/{self.get_user(self.u_dict).username}',
                          data=json.dumps({
                              'username': 'new_test_u',
                              'password': 'new_test_p',
                              'email': 'new_test_u@test_o.com',
                              'organization_id': self.u_dict['organization_id'],
                              'is_super': True,
                              'is_owner': True
                          }),
                          headers=self.get_headers())

                user = json.loads(r.data)['user']
                self.assertEqual(user['username'],
                                 'new_test_u')
                self.assertEqual(user['email'],
                                 'new_test_u@test_o.com')
                self.assertEqual(user['organization_id'],
                                 self.u_dict['organization_id'])
                self.assertTrue(user['is_super'])
                self.assertTrue(user['is_owner'])
                self.assertTrue(user['is_active'])
                self.assertEqual(r.status_code, 200)

    def test_user_put_without_authentication(self):
        """
        Test that a PUT request to the /user/<string:username> endpoint returns
        status code 401 if the user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send PUT request to the /user/test_u endpoint with
                # wrong authentication header.
                r = c.put(f'/user/{self.get_user(self.u_dict).username}',
                          data=json.dumps({
                              'username': 'new_test_u',
                              'password': 'new_test_p',
                              'email': 'new_test_u@test_o.com',
                              'organization_id': self.u_dict['organization_id'],
                              'is_super': True,
                              'is_owner': True
                          }),
                          headers={
                              'Content-Type': 'application/json',
                              'Authorization': 'JWT FaKeToKeN!!'
                          })

                self.assertEqual(r.status_code, 401)

    def test_user_put_not_found(self):
        """
        Test that a PUT request to the /user/<string:username> endpoint returns
        status code 404 if the user is not in the database.
        """
        with self.app() as c:
            with self.app_context():
                r = c.put(f'/user/{self.u_dict["username"]}',
                          data=json.dumps({
                              'username': 'new_test_u',
                              'password': 'new_test_p',
                              'email': 'new_test_u@test_o.com',
                              'organization_id': self.u_dict['organization_id'],
                              'is_super': True,
                              'is_owner': True
                          }),
                          headers=self.get_headers())

                self.assertEqual(r.status_code, 404)

    def test_user_delete_with_authentication(self):
        """
        Test that a DELETE request to the /user/<string:username>
        endpoint returns status code 200.
        """
        with self.app() as c:
            with self.app_context():
                r = c.delete(f'/user/{self.get_user(self.u_dict).username}',
                             headers=self.get_headers())

                self.assertEqual(r.status_code, 200)

    def test_user_delete_without_authentication(self):
        """
        Test that a DELETE request to the /user/<string:username> endpoint
        returns status code 401 if user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send DELETE request to the /user/test_u endpoint
                # with wrong authorization header.
                r = c.delete(f'/user/{self.get_user(self.u_dict).username}',
                             headers={
                                 'Content-Type': 'application/json',
                                 'Authorization': 'JWT FaKeToKeN!!'
                             })

                self.assertEqual(r.status_code, 401)

    def test_user_delete_inactive(self):
        """
        Test that a DELETE request to the /user/<string:username> endpoint
        returns status code 400 if the user is already inactive.
        """
        with self.app() as c:
            with self.app_context():
                username = self.get_user(self.u_dict).username

                # Make user inactive.
                c.delete(f'/user/{username}',
                         headers=self.get_headers())

                # Send DELETE request on inactive user.
                r = c.delete(f'/user/{username}',
                             headers=self.get_headers())

                self.assertEqual(r.status_code, 400)

    def test_user_delete_not_found(self):
        """
        Test that a DELETE request to the /user/<string:username>
        endpoint returns status code 404 if the user is not found.
        """
        with self.app() as c:
            with self.app_context():
                r = c.delete(f'/user/{self.u_dict["username"]}',
                             headers=self.get_headers())

                self.assertEqual(r.status_code, 404)

    def test_activate_user_with_authentication(self):
        """
        Test that a PUT request to the /activate_user/<string:username>
        endpoint returns status code 200.
        """
        with self.app() as c:
            with self.app_context():
                username = self.get_user(self.u_dict).username

                c.delete(f'/user/{username}',
                         headers=self.get_headers())

                r = c.put(f'/activate_user/{username}',
                          headers=self.get_headers())

                self.assertEqual(r.status_code, 200)

    def test_activate_user_without_authentication(self):
        """
        Test that a PUT request to the /activate_user/<string:username>
        endpoint returns status code 401 if the user is not authenticated.
        """
        with self.app() as c:
            with self.app_context():
                # Send PUT request to /activate_user/test_u with
                # wrong authorization header.
                r = c.put(f'/activate_user/'
                          f'{self.get_user(self.u_dict).username}',
                          headers={
                              'Content-Type': 'application/json',
                              'Authorization': 'JWT FaKeToKeN!!'
                          })

                self.assertEqual(r.status_code, 401)

    def test_activate_user_active(self):
        """
        Test that a PUT request to the /activate_user/<string:username>
        endpoint returns status code 400 if the user is already active.
        """
        with self.app() as c:
            with self.app_context():
                r = c.put(f'/activate_user/'
                          f'{self.get_user(self.u_dict).username}',
                          headers=self.get_headers())

                self.assertEqual(r.status_code, 400)

    def test_activate_user_not_found(self):
        """
        Test that a PUT request to the /activate_user/<string:username>
        endpoint returns status code 404 if the user is not found.
        """
        with self.app() as c:
            with self.app_context():
                r = c.put(f'/activate_user/'
                          f'{self.u_dict["username"]}',
                          headers=self.get_headers())

                self.assertEqual(r.status_code, 404)
