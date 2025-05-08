import unittest
from selenium import webdriver

class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_todo_list(self):
        # I heard about a cool new online to-do app. 
        # so I went to check out its home page
        self.browser.get("http://localhost:8000")

        #Here is where I notice the page title and header 
        self.assertIn("To-Do", self.browser.title)

        # I am invited to enter a to-do item straight away
        self.fail("Finish the test!")


#I type in "make some slides"

#When I hit enter, the page updates, and now the page 
#lists "make some slides" as an item
if __name__ == "__main__":
    unittest.main()