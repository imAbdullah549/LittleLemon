from django.test import TestCase
from django.urls import reverse
from .models import Category, Menu

class MenuListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Category.objects.create(slug='test-category', title='Test Category')

        for i in range(1, 6):
            Menu.objects.create(
                title=f'Test Menu {i}', 
                price=i * 10.50, 
                featured=i % 2 == 0, 
                category=Category.objects.get(slug='test-category')
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/menu/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('menu-list'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('menu-list'))
        self.assertTemplateUsed(response, 'menu/menu_list.html')

    def test_view_displays_menus(self):
        response = self.client.get(reverse('menu-list'))
        self.assertContains(response, 'Test Menu 1')
        self.assertContains(response, 'Test Menu 2')
        self.assertContains(response, 'Test Menu 3')
        self.assertContains(response, 'Test Menu 4')
        self.assertContains(response, 'Test Menu 5')
