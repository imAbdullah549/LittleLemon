from django.test import TestCase
from Resturant.models import Category, Menu

class MenuModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Category.objects.create(slug='test-category', title='Test Category')

    def test_title_max_length(self):
        menu = Menu.objects.create(
            title='A' * 256, 
            price=10.50, 
            featured=True, 
            category=Category.objects.get(slug='test-category')
        )
        max_length = menu._meta.get_field('title').max_length
        self.assertEquals(max_length, 255)

    def test_category_relationship(self):
        category = Category.objects.get(slug='test-category')
        menu = Menu.objects.create(
            title='Test Menu', 
            price=10.50, 
            featured=True, 
            category=category
        )
        self.assertEquals(menu.category, category)

    def test_price_max_digits(self):
        menu = Menu.objects.create(
            title='Test Menu', 
            price=9999.99, 
            featured=True, 
            category=Category.objects.get(slug='test-category')
        )
        max_digits = menu._meta.get_field('price').max_digits
        self.assertEquals(max_digits, 6)

    def test_price_decimal_places(self):
        menu = Menu.objects.create(
            title='Test Menu', 
            price=10.555, 
            featured=True, 
            category=Category.objects.get(slug='test-category')
        )
        decimal_places = menu._meta.get_field('price').decimal_places
        self.assertEquals(decimal_places, 2)

    def test_featured_default_value(self):
        menu = Menu.objects.create(
            title='Test Menu', 
            price=10.50, 
            category=Category.objects.get(slug='test-category')
        )
        self.assertFalse(menu.featured)
