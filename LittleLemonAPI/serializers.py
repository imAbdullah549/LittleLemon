from rest_framework import serializers
from .models import MenuItem,Category,Cart,Order,OrderItem
from rest_framework.validators import UniqueTogetherValidator
from django.contrib.auth.models import User

# Category Serializer

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','title']

# Menu Serializer

class MenuItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)  # Nested CategorySerializer for GET request
    category_id = serializers.IntegerField(
        write_only=True
    )
    class Meta:
        model = MenuItem
        fields = ['id','title','price','featured','category','category_id']
        validators=[
        UniqueTogetherValidator(
        queryset=MenuItem.objects.all(),
        fields=['title', 'category_id']
        )
        ]

# Cart Serializer

class CartSerializer(serializers.ModelSerializer):
    menuitem = MenuItemSerializer(read_only=True)  
    menuitem_id = serializers.IntegerField(
        write_only=True
    )
    class Meta:
        model = Cart
        fields = ['user','menuitem','quantity','unit_price','price',"menuitem_id"]

# Order Serializer

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id','user', 'delivery_crew', 'status', 'total', 'date']



class OrderItemSerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only=True)  # Nested OrderSerializer for GET request
    order_id = serializers.PrimaryKeyRelatedField(
        queryset=Order.objects.all(),
        write_only=True,
        source='order'
    )

    class Meta:
        model = OrderItem
        fields = ['order', 'order_id', 'menuitem', 'quantity', 'unit_price', 'price']


