from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User, Group
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import MenuItem,Category,Cart,Order,OrderItem
from .serializers import MenuItemSerializer, CategorySerializer, CartSerializer,OrderSerializer,OrderItemSerializer
from rest_framework.permissions import IsAuthenticated,BasePermission
import datetime



class ManagerGroupPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.groups.filter(name='Manager').exists() or request.user.is_superuser


class ManagerGroupView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        if request.user.groups.filter(name='Manager').exists() or request.user.is_superuser:
            group = Group.objects.get(name='Manager')
            users = group.user_set.all()
            return Response(users.values())
        else:
            return Response({'error': 'You are not authorized to access this view.'}, status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request):
        username = request.data.get('username')
        user = get_object_or_404(User, username=username)
        if request.user.groups.filter(name='Manager').exists() or request.user.is_superuser:
            group = Group.objects.get(name='Manager')
            user.groups.add(group)
            return Response({'message': 'User added to the Manager group.'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'You are not authorized to access this view.'}, status=status.HTTP_401_UNAUTHORIZED)
        
    def delete(self, request, id):
        user = get_object_or_404(User, id=id)
        if user.groups.filter(name="Manager").exists():
            if request.user.groups.filter(name="Manager").exists():
                group = Group.objects.get(name='Manager')
                user.groups.remove(group)
                return Response({'message': 'User removed from the Manager group.'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'You are not authorized to access this view.'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'The provided ID does not belong to the Manager group.'}, status=status.HTTP_404_NOT_FOUND)


class deliveryCrewGroupView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        if request.user.groups.filter(name='Manager').exists() or request.user.is_superuser:
            group = Group.objects.get(name='DeliveryCrew')
            users = group.user_set.all()
            return Response(users.values())
        else:
            return Response({'error': 'You are not authorized to access this view.'}, status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request):
        username = request.data.get('username')
        user = get_object_or_404(User, username=username)
        if request.user.groups.filter(name='Manager').exists() or request.user.is_superuser:
            group = Group.objects.get(name='DeliveryCrew')
            user.groups.add(group)
            return Response({'message': 'User added to the delivery crew group.'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'You are not authorized to access this view.'}, status=status.HTTP_401_UNAUTHORIZED)
            
    def delete(self, request, id):
        print("in delete view")
        user = get_object_or_404(User, id=id)
        print("user",user)
        if user.groups.filter(name="DeliveryCrew").exists():
            if request.user.groups.filter(name="Manager").exists():
                group = Group.objects.get(name='DeliveryCrew')
                user.groups.remove(group)
                return Response({'message': 'User removed from the delivery crew group.'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'You are not authorized to access this view.'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'The provided ID does not belong to the delivery crew group.'}, status=status.HTTP_404_NOT_FOUND)


# Category Views

class categoryView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if(self.request.method=='GET'):
            return []
        return [IsAuthenticated(), ManagerGroupPermission()]


class singleCategoryView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if(self.request.method=='GET'):
            return []
        return [IsAuthenticated(), ManagerGroupPermission()]


    
class menuItemView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    ordering_fileds = ['price','title','category']
    filterset_fields = ['price','feature','category']
    search_fields = ['category','title']

    def get_permissions(self):
        if(self.request.method=='GET'):
            return []
        return [IsAuthenticated(), ManagerGroupPermission()]


class singleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def get_permissions(self):
        if(self.request.method=='GET'):
            return []
        return [IsAuthenticated(), ManagerGroupPermission()]

# cart view 
class cartView(generics.GenericAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def get(self, request):
        user = self.request.user
        cart_items = Cart.objects.filter(user=user)
        serializer = CartSerializer(cart_items, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        user = self.request.user
        Cart.objects.filter(user=user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
# Order view 
class OrderView(generics.ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='DeliveryCrew').exists():
            orders = Order.objects.filter(delivery_crew=user)
        else:
            orders = Order.objects.filter(user=user)
        return orders

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data

        # Retrieve related OrderItem objects for each Order
        for i, order_data in enumerate(data):
            order = queryset[i]
            order_items = order.orderitem_set.all()
            order_item_serializer = OrderItemSerializer(order_items, many=True)
            order_data['order_items'] = order_item_serializer.data

        return Response(data)

    def post(self, request):
        user = self.request.user
        cart_items = Cart.objects.filter(user=user)

        # Create the order instance
        order_data = {
            'user': user.pk,
            'delivery_crew': None,
            'status': False,
            'total': 0,
            'date': datetime.date.today()
        }
        order_serializer = OrderSerializer(data=order_data)
        if order_serializer.is_valid():
            order = order_serializer.save()
        else:
            errors = order_serializer.errors
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        order_items = []
        for cart_item in cart_items:
            order_item_data = {
                'order_id': order.pk,
                'menuitem': cart_item.menuitem.pk,
                'quantity': cart_item.quantity,
                'unit_price': cart_item.unit_price,
                'price': cart_item.price
            }
            order_item_serializer = OrderItemSerializer(data=order_item_data)
            if order_item_serializer.is_valid():
                order_item_serializer.save()
                order_items.append(order_item_serializer.data)
            else:
                errors = order_item_serializer.errors
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(order_serializer.data, status=status.HTTP_201_CREATED)



class singleOrderView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_permissions(self):
        if(self.request.method=='GET'):
            return []
        elif self.request.method == 'PATCH' and self.request.user.groups.filter(name='DeliveryCrew').exists():
            return []  
        else:
            return [IsAuthenticated(), ManagerGroupPermission()]
        

