from django.contrib import admin
from .models import Plan, UserProfile, Category, Product, Sale
from django.contrib.auth.models import User, Group

try:
  admin.site.unregister(User)
except admin.exceptions.NotRegistered:
  pass

try:
  admin.site.unregister(Group)
except admin.exceptions.NotRegistered:
  pass

admin.site.register(User)
admin.site.register(Plan)
admin.site.register(UserProfile)
admin.site.register(Category)
admin.site.register(Sale)

# 2. Registro com Personalização (para o Produto)
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # O Admin usará estas configurações:
    list_display = ('name', 'quantity_total', 'quantity_sold', 'quantity_in_stock', 'sale_value', 'total_profit')
    list_filter = ('category', 'sale_value')
    search_fields = ('name', 'observation')
