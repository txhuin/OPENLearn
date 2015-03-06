import unittest
import sys
import model
# sys.path.append('/Users/Gaikwad/HB-FinalProject')
# # from HBFinalProject import recommender
# # import os,sys,inspect
# # currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
# # parentdir = os.path.dirname(currentdir)
# # sys.path.insert(0,parentdir) 

# app = recommender.app.test_client()

result = app.get('/')

def load_tests(loader, tests, ignore):
    """Also run our doctests and file-based doctests.

    This function name, ``load_tests``, is required.
    """

    tests.addTests(doctest.DocTestSuite(recommender))
    tests.addTests(doctest.DocFileSuite("tests.txt"))
    return tests


class MyAppIntegrationTestCase(unittest.TestCase):

	def setUp(self):
	    self.app = recommender.app.test_client()

	def testhomepage(self):
	   	result = self.app.get("/")
		self.assertEqual(result.status_code, 200)
		self.assertIn('<h2>Discover your next great MOOC.</h2>', result.data)
	    # self.assertIn

	def testresultspage(self):
	    result = self.app.get("/Recommend")
	    self.assertEqual(result.status_code, 200)
	    	# self.assertIn('')

	def testprofilepage(self):
	    result = self.app.get('/myprofile')
	    self.assertEqual(result.status_code, 200)


# class MyTest(unittest.TestCase):

# 	self.assertEqual(result.status_code, 200)



if __name__ == "__main__":
	unittest.main()