from django.db import models
from django.db.models import Sum

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    class Meta:
        verbose_name_plural = "Categorias"

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=130)
    observation = models.CharField(max_length=200,blank=True,null=True)
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,related_name='category',null=True)
    
    # Renamed/New fields for quantity tracking
    quantity_total = models.IntegerField(default=0, verbose_name="Quantidade Comprada")
    
    # Prices
    cost = models.DecimalField(max_digits=10,decimal_places=2)
    sale_value = models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True,default=0)
    
    cadastred_date = models.DateTimeField(auto_now_add=True)
    
    @property
    def quantity_sold(self):
        # Sum quantities from related Sale records
        return self.sales.aggregate(total=Sum('quantity'))['total'] or 0

    @property
    def quantity_in_stock(self):
        return self.quantity_total - self.quantity_sold
    
    @property
    def is_sold_out(self):
        return self.quantity_in_stock <= 0

    @property
    def average_sale_price(self):
        """Calculate average price from actual sales"""
        if self.quantity_sold > 0:
            # Calculate total revenue from all sales (price_sold * quantity for each sale)
            total_revenue = sum(sale.price_sold * sale.quantity for sale in self.sales.all())
            return total_revenue / self.quantity_sold
        return self.sale_value or 0
    
    @property
    def total_profit(self):
        """Calculate total profit from actual sales"""
        if self.quantity_sold > 0:
            # Calculate total revenue from all sales (price_sold * quantity for each sale)
            total_revenue = sum(sale.price_sold * sale.quantity for sale in self.sales.all())
            total_cost = self.cost * self.quantity_sold
            return total_revenue - total_cost
        return 0
    
    @property
    def unit_profit(self):
        """Calculate profit per unit based on average sale price"""
        return self.average_sale_price - self.cost
    
    @property
    def profit(self):
        """Legacy property - returns unit profit based on sale_value"""
        if self.sale_value is None or self.sale_value == 0:
            return self.unit_profit
        else:
            return self.sale_value - self.cost
    
    def __str__(self):
        return f"{self.name} | Estoque: {self.quantity_in_stock}" 

class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sales')
    quantity = models.IntegerField(default=1)
    price_sold = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Venda: {self.product.name} (x{self.quantity})"
