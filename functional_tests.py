import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

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
        header_text = self.browser.find_element(By.TAG_NAME, "h1").text
        self.assertIn("To-Do", header_text)

        # I am invited to enter a to-do item straight away
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        self.assertEqual(inputbox.get_attribute("placeholder"), "Enter a to-do item")

        #I type in "make some slides"
        inputbox.send_keys("Make some slides")

        #When I hit enter, the page updates, and now the page 
        #lists "make some slides" as an item
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        table = self.browser.find_element(By.ID, "id_list_table")
        rows = table.find_elements(By.TAG_NAME, "tr")
        self.assertIn("1: Make some slides", 
                      [row.text for row in rows])

        self.assertIn("2: Drink a coffee", 
                      [row.text for row in rows])

        #there is still a text box inviting me to add another item.
        #enter "read the textbook"
        self.fail("finish the test")

        #the page updates again and shows both items on my list
if __name__ == "__main__":
    unittest.main()