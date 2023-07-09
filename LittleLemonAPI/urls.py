from django.urls import path
from . import views

urlpatterns = [
    path('groups/manager/users',views.ManagerGroupView.as_view()),
    path("groups/manager/users/<int:id>",views.ManagerGroupView.as_view()), 
    path('groups/delivery-crew/users',views.deliveryCrewGroupView.as_view()),
    path("groups/delivery-crew/users/<int:id>",views.deliveryCrewGroupView.as_view()),     
    path("category",views.categoryView.as_view()), 
    path("category/<int:pk>",views.singleCategoryView.as_view()),
    path("menu-items",views.menuItemView.as_view()),
    path("menu-items/<int:pk>",views.singleMenuItemView.as_view()),
    path("cart/menu-items",views.cartView.as_view()),
    path("orders",views.OrderView.as_view()),
    path("orders/<int:pk>",views.singleOrderView.as_view()),      
]
