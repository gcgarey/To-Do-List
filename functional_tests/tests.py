import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from django.test import LiveServerTestCase
from selenium.common.exceptions import WebDriverException

MAX_WAIT = 5

class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try: 
                table = self.browser.find_element(By.ID, 
                                                  "id_list_table")
                rows = table.find_elements(By.TAG_NAME, "tr")
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException):
                if time.time() - start_time > MAX_WAIT:
                    raise
                time.sleep(0.5)

    def test_can_start_a_todo_list(self):
        # I heard about a cool new online to-do app. 
        # so I went to check out its home page
        self.browser.get(self.live_server_url)

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
        self.wait_for_row_in_list_table("1: Make some slides")

        #there is still a text box inviting me to add another item.
        #enter "read the textbook"
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        inputbox.send_keys("read the textbook")
        inputbox.send_keys(Keys.ENTER)


        #the page updates again and shows both items on my list
        self.wait_for_row_in_list_table("1: Make some slides")
        self.wait_for_row_in_list_table("2: read the textbook")

        # Good. I will go back to sleep now

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # I start a new to-do list
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        inputbox.send_keys("make some slides")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: make some slides")

        # I notice that my list has a unique url
        my_list_url = self.browser.current_url
        self.assertRegex(my_list_url, "/lists/.+") # from unittest. Does string match expression

        # Now a new user, Carol, comes along to the site. 

        # We delete all the browser's cookies
        # as a way of simulating a brand new user session
        self.browser.delete_all_cookies()

        # Carol visits the home page. There is no sign of
        # my list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element(By.ID, "id_new_item")
        self.assertNotIn("make some slides", page_text)
        self.assertNotIn("make a fly", page_text)

        # Carol starts a new list by entering a new item. 
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        inputbox.send_keys("buy milk")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: buy milk")

        # Carol gets her own unique URL
        carol_list_url = self.browser.current_url
        self.assertRegex(carol_list_url, "/lists/.+")
        self.assertNotEqual(carol_list_url, my_list_url)

        # Again, there is no trace of my list
        page_text = self.browser.find_element(By.TAG_NAME, "body").text
        self.assertNotIn("make some slides", page_text)
        self.assertIn("buy milk", page_text)

        # Satisfied, they both go back to sleep



if __name__ == "__main__":
    unittest.main()