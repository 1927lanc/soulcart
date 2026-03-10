from django.urls import path
from . import views

urlpatterns = [
    path('', views.CartView.as_view(), name='cart'),
    path('update/<int:item_id>/', views.UpdateCartItemView.as_view(), name='cart-update'),
]