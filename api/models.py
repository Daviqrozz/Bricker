from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django_multitenant.models import TenantModel, TenantManager
from django_multitenant.fields import TenantForeignKey


def get_tenant_value(self):
    return self.id


User.tenant_value = property(get_tenant_value)


class Plan(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    max_products = models.IntegerField(default=50)
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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

    def __str__(self):
        return self.name


class Product(TenantModel):

    class Status(models.TextChoices):
        AVAILABLE = 'available', 'Disponível'
        SOLD      = 'sold',      'Vendido'

    user     = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_products')
    name     = models.CharField(max_length=130)
    observation = models.CharField(max_length=200, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='products', null=True)
    status   = models.CharField(max_length=20, choices=Status.choices, default=Status.AVAILABLE)
    cost     = models.DecimalField(max_digits=10, decimal_places=2)
    expected_sale_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    tenant_id = 'user_id'
    objects   = TenantManager()

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
        ordering = ['-created_at']
        constraints = [models.UniqueConstraint(fields=['id', 'user'], name='unique_product_tenant')]

    @property
    def is_available(self):
        return self.status == self.Status.AVAILABLE

    @property
    def profit(self):
        if self.expected_sale_value:
            return self.expected_sale_value - self.cost
        return 0

    def __str__(self):
        return self.name


class Sale(TenantModel):
    user       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_sales')
    product    = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='sale')
    price_sold = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    tenant_id = 'user_id'
    objects   = TenantManager()

    class Meta:
        verbose_name = "Venda"
        verbose_name_plural = "Vendas"
        ordering = ['-created_at']
        constraints = [models.UniqueConstraint(fields=['id', 'user'], name='unique_sale_tenant')]

    @property
    def profit(self):
        return self.price_sold - self.product.cost

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