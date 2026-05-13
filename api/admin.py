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
    list_display = ('name', 'category', 'status', 'cost', 'expected_sale_value', 'profit')
    list_filter = ('category', 'status')
    search_fields = ('name', 'observation')
