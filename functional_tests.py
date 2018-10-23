from selenium import  webdriver
import unittest
import time
from selenium.webdriver.common.keys import Keys

class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.brower=webdriver.Chrome()

    def tearDown(self):
        self.brower.quit()


    def checheck_for_row_in_list_tableck(self,row_text):
        table=self.brower.find_element_by_id('id_list_table')
        rows=table.find_element_by_tag_name('tr')

    def test_can_start_a_list_and_retrieve_it_later(self):

        self.brower.get("http://localhost:8000/")
        self.assertIn("To-Do",self.brower.title)
        header_text=self.brower.find_element_by_tag_name('h1').text
        self.assertIn('To-Do',header_text)

        inptbox=self.brower.find_element_by_id('id_new_item')
        self.assertEqual(
            inptbox.get_attribute('placeholder'),
            'enter a to-do item'
        )
        inptbox.send_keys('Buy peacock feathers')

        inptbox.send_keys(Keys.ENTER)
        time.sleep(1)

        table=self.brower.find_element_by_id('id_list_table')
        rows=table.find_element_by_tag_name('tr')
        self.assertIn('1: Buy peacock feathers', [row.text for row in rows])
        self.fail('finsh the test')

if __name__ == '__main__':
        unittest.main(warnings='ignore')
#
# #最后是 if __name__ == '__main__' 分句（如果你之前没见过这种用法，我告诉你，Python 脚本使用这个语句检查自己是否在命令行中运行，而不是在其他脚本中导入）。我们调用 unittest.main() 启动 unittest 的测试运行程序，这个程序会在文件中自动查找测试类和方法，然后运行。
#warnings='ignore' 的作用是禁止抛出 ResourceWarning 异常。写作本书时这个异常会抛 出，但你阅读时我可能已经把这个参数去掉了。你可以把这个参数删掉，看一下效果。