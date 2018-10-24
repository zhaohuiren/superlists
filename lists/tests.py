from django.test import TestCase
from django.urls import resolve
from lists.views import home_page
import requests
from django.template.loader import render_to_string
from django.http import HttpRequest
from lists.models import Item
# Create your tests here.
class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found=resolve('/')
        self.assertEqual(found.func,home_page)

    # def test_home_page_returns_correct_html(self):
    #
    #     request=HttpRequest()#创建request对象
    #     response=home_page(request)#把httprequest传给homepage视图
    #     html=response.content.decode('utf8')#转成html
    #     self.assertTrue(html.startswith('<html>'))#断言响应起始标签
    #     self.assertIn('<title>To-Do lists</title>', html)
    #     self.assertTrue(html.strip().endswith('</html>'))#断言结束起始标签

    # def test_home_page_returns_correct_html(self):
    #     response=self.client.get('/')#传入url
    #     html= response.content.decode('utf8')
    #     self.assertTrue(html.startswith('<html>'))
    #     self.assertIn('<title>To-Do lists</title>', html)
    #     self.assertTrue(html.strip().endswith('</html>'))
    #     self.assertTemplateUsed(response, 'home.html')

    def test_uses_home_template(self):
        response = self.client.get('/')

        self.assertTemplateUsed(response, 'home.html')

    def test_can_save_a_POST_request(self):
        response=self.client.post('/',data={'item_text': 'A new list item'})

        self.assertEqual(Item.objects.count(),1)
        new_item=Item.objects.first()
        self.assertEqual(new_item.text,'A new list item')

#重定向
    def test_redirects_after_POST(self):
        response = self.client.post('/', data={'item_text': 'A new list item'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'],  '/lists/the-only-list-in-the-world/')



    # def test_only_saves_items_when_necessary(self):
    #     self.client.get('/')
    #     self.assertEqual(Item.objects.count(), 0)0



    def home_page(request):
        if request.method=='POST':
            new_item_text=request.POST['item_text']
            Item.objects.create(text=new_item_text)
        else:
            new_item_text=''

        return render(request,'home.html', {'new_item_text': new_item_text, })

#测试清单
    def test_displays_all_list_items(self):
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')

        response = self.client.get('/')

        self.assertIn('itemey 1', response.content.decode())
        self.assertIn('itemey 2', response.content.decode())



class ItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        first_item=Item()
        first_item.text='The first (ever) list item'
        first_item.save()

        second_item=Item()
        second_item.text = 'Item the second'
        second_item.save()

        saved_items=Item.objects.all()
        self.assertEqual(saved_items.count(),2)

        first_saved_item=saved_items[0]
        second_saved_item=saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(second_saved_item.text, 'Item the second')

class ListViewTest(TestCase):
    def test_displays_all_items(self):
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')

        response = self.client.get('/lists/the-only-list-in-the-world/')

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')