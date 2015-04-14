import unittest
import model
import recommender

class Usersignup(unittest.TestCase):
	"""Tests if a user can sign up"""

	def setUp(self):
		self.app = recommender.app.test_client()

	def test_home(self):
		result = self.app.get('/')
		self.assertIn('<h1>Discover your next great online course</h1>', result.data)
		self.assertEqual(result.status_code, 200)



if __name__ =="__main__":
	unittest.main()