from django.db import models
from django.db.models import Sum
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

class Plan(models.Model):
  name = models.CharField(max_length=50, unique=True)
  description = models.TextField(blank=True, null=True)
  price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
  max_products = models.IntegerField(default=50, help_text="Limite de produtos para este plano")
  is_active = models.BooleanField(default=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    verbose_name = "Plano"
    verbose_name_plural = "Planos"

  def __str__(self):
    return self.name

  @property
  def is_free(self):
    return self.price == 0

class UserProfile(models.Model):
  user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
  onboarding_completed_at = models.DateTimeField(null=True, blank=True)
  plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True, blank=True, related_name='profiles')
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    verbose_name = "Perfil"
    verbose_name_plural = "Perfis"

  def __str__(self):
    return self.user.username

class Category(models.Model):
  name = models.CharField(max_length=100)
  description = models.TextField(blank=True, null=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    verbose_name = "Categoria"
    verbose_name_plural = "Categorias"

  def __str__(self):
    return self.name

class Product(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  name = models.CharField(max_length=130)
  observation = models.CharField(max_length=200, blank=True, null=True)
  category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='products', null=True)
  quantity_total = models.IntegerField(default=0, verbose_name="Quantidade Comprada")
  cost = models.DecimalField(max_digits=10, decimal_places=2)
  sale_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    verbose_name = "Produto"
    verbose_name_plural = "Produtos"

  @property
  def quantity_sold(self):
    return self.sales.aggregate(total=Sum('quantity'))['total'] or 0

  @property
  def quantity_in_stock(self):
    return self.quantity_total - self.quantity_sold

  @property
  def is_sold_out(self):
    return self.quantity_in_stock <= 0

  @property
  def average_sale_price(self):
    if self.quantity_sold > 0:
      total_revenue = sum(sale.price_sold * sale.quantity for sale in self.sales.all())
      return total_revenue / self.quantity_sold
    return self.sale_value or 0

  @property
  def total_profit(self):
    if self.quantity_sold > 0:
      total_revenue = sum(sale.price_sold * sale.quantity for sale in self.sales.all())
      total_cost = self.cost * self.quantity_sold
      return total_revenue - total_cost
    return 0

  @property
  def unit_profit(self):
    return self.average_sale_price - self.cost

  @property
  def profit(self):
    if self.sale_value is None or self.sale_value == 0:
      return self.unit_profit
    else:
      return self.sale_value - self.cost

  def __str__(self):
    return self.name

class Sale(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_sales')
  product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sales')
  quantity = models.IntegerField(default=1)
  price_sold = models.DecimalField(max_digits=10, decimal_places=2)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    verbose_name = "Venda"
    verbose_name_plural = "vendas"

  def __str__(self):
    return self.product.name

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
  if created:
    default_plan = Plan.objects.filter(id=1).first() or Plan.objects.first()
    UserProfile.objects.create(user=instance, plan=default_plan)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
  instance.profile.save()
