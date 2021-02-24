import shopify
from test.test_helper import TestCase


class UserTest(TestCase):
    def test_get_all_users(self):
        self.fake('users', body=self.load_fixture('users'))
        users = shopify.User.find()

        self.assertEqual(2, len(users))
        self.assertEqual("Steve", users[0].first_name)
        self.assertEqual("Jobs", users[0].last_name)

    def test_get_user(self):
        self.fake('users/799407056', body=self.load_fixture('user'))
        user = shopify.User.find(799407056)

        self.assertEqual("Steve", user.first_name)
        self.assertEqual("Jobs", user.last_name)

    def test_get_current_user(self):
        self.fake('users/current', body=self.load_fixture('user'))
        user = shopify.User.current()

        self.assertEqual("Steve", user.first_name)
        self.assertEqual("Jobs", user.last_name)
