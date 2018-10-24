from selenium import  webdriver
import unittest
import time
from django.test import LiveServerTestCase
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
MAX_WAIT = 10
class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser=webdriver.Chrome()

    def wait_for_row_in_list_table(self, row_text):

        start_time = time.time()

        while True:

            try:

                table = self.browser.find_element_by_id('id_list_table')

                rows = table.find_elements_by_tag_name('tr')

                self.assertIn(row_text, [row.text for row in rows])

                return

            except (AssertionError, WebDriverException) as e:

                if time.time() - start_time > MAX_WAIT:
                    raise e

                time.sleep(0.5)
    def test_can_start_a_list_and_retrieve_it_later(self):


        self.browser.get(self.live_server_url)

        self.assertIn('To-Do', self.browser.title)

        header_text = self.browser.find_element_by_tag_name('h1').text

        self.assertIn('To-Do', header_text)



        inputbox = self.browser.find_element_by_id('id_new_item')

        self.assertEqual(inputbox.get_attribute('placeholder'),'Enter a to-do item')



        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table('1: Buy peacock feathers')



        inputbox = self.browser.find_element_by_id('id_new_item')

        inputbox.send_keys('Use peacock feathers to make a fly')

        inputbox.send_keys(Keys.ENTER)



        self.wait_for_row_in_list_table('2: Use peacock feathers to make a fly')

        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        self.fail('Finish the test!')


    def test_can_start_a_list_for_one_user(self):
        self.browser.get(self.live_server_url)
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)
        self.wait_for_row_in_list_table('2: Use peacock feathers to make a fly')
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

    def test_multiple_users_can_start_lists_at_different_urls(self):

        # Edith starts a new to-do list

        self.browser.get(self.live_server_url)

        inputbox = self.browser.find_element_by_id('id_new_item')

        inputbox.send_keys('Buy peacock feathers')

        inputbox.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        # She notices that her list has a unique URL

        edith_list_url = self.browser.current_url

        self.assertRegex(edith_list_url, '/lists/.+')


        self.browser.quit()

        self.browser = webdriver.Firefox()

        self.browser.get(self.live_server_url)

        page_text = self.browser.find_element_by_tag_name('body').text

        self.assertNotIn('Buy peacock feathers', page_text)

        self.assertNotIn('make a fly', page_text)

        inputbox = self.browser.find_element_by_id('id_new_item')

        inputbox.send_keys('Buy milk')

        inputbox.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table('1: Buy milk')

        francis_list_url = self.browser.current_url

        self.assertRegex(francis_list_url, '/lists/.+')

        self.assertNotEqual(francis_list_url, edith_list_url)

        page_text = self.browser.find_element_by_tag_name('body').text

        self.assertNotIn('Buy peacock feathers', page_text)

        self.assertIn('Buy milk', page_text)



#
    def tearDown(self):
        self.browser.quit()
# #最后是 if __name__ == '__main__' 分句（如果你之前没见过这种用法，我告诉你，Python 脚本使用这个语句检查自己是否在命令行中运行，而不是在其他脚本中导入）。我们调用 unittest.main() 启动 unittest 的测试运行程序，这个程序会在文件中自动查找测试类和方法，然后运行。
#warnings='ignore' 的作用是禁止抛出 ResourceWarning 异常。写作本书时这个异常会抛 出，但你阅读时我可能已经把这个参数去掉了。你可以把这个参数删掉，看一下效果。