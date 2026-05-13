
from django.urls import path
from .views import product_view, create_view, edit_view, delete_view, sell_product_view, update_onboarding_preference

urlpatterns = [
  path('', product_view, name='products_view'),
  path('create', create_view, name='create_view'),
  path('edit/<int:id>/', edit_view, name='edit_view'),
  path('delete/<int:id>', delete_view, name='delete_view'),
  path('sell/<int:id>/', sell_product_view, name='sell_product_view'),
  path('update-onboarding/', update_onboarding_preference, name='update_onboarding'),
]
