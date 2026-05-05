
from django.urls import path
from .views import product_view, create_view, edit_view, create_category_view, delete_view, sell_product_view

urlpatterns = [
  path('', product_view, name='products_view'),
  path('create', create_view, name='create_view'),
  path('create_category', create_category_view, name='create_category_view'),
  path('edit/<int:id>/', edit_view, name='edit_view'),
  path('delete/<int:id>', delete_view, name='delete_view'),
  path('sell/<int:id>/', sell_product_view, name='sell_product_view'),
]
