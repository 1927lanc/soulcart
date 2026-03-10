from django.urls import path
from . import views

urlpatterns = [
    path('place/', views.PlaceOrderView.as_view(), name='place-order'),
    path('', views.OrderListView.as_view(), name='order-list'),
    path('<int:order_id>/', views.OrderDetailView.as_view(), name='order-detail'),
]