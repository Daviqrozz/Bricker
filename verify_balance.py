import os
import django
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'revenda_estoque.settings')
django.setup()

from api.models import Product, Sale, Category

def calculate_balance():
    """Calculate profit from sales in the last 30 days"""
    thirty_days_ago = timezone.now() - timedelta(days=30)
    
    # Get sales from the last 30 days
    recent_sales = Sale.objects.filter(created_at__gte=thirty_days_ago)
    
    # Calculate total revenue from sales
    total_sales = recent_sales.aggregate(total=Sum('price_sold'))['total'] or 0
    
    # Calculate total cost for sold items (cost per unit * quantity sold)
    total_cost = 0
    for sale in recent_sales:
        total_cost += sale.product.cost * sale.quantity
    
    balance = total_sales - total_cost
    return balance

print("--- Start Verification (v2.0.0) ---")
initial_balance = calculate_balance()
print(f"Initial Balance: R$ {initial_balance:.2f}")

# Add a new product and make a sale
print("\nAdding new product (Cost: R$ 100, Quantity: 10)...")
category, _ = Category.objects.get_or_create(name="Teste")
new_product = Product.objects.create(
    name="Test Product v2",
    cost=100.00,
    sale_value=150.00,
    quantity_total=10,
    category=category
)
print(f"Product created: {new_product.name} | Stock: {new_product.quantity_in_stock}")

# Make a sale
print("\nMaking a sale (Quantity: 3, Price: R$ 150 each)...")
new_sale = Sale.objects.create(
    product=new_product,
    quantity=3,
    price_sold=150.00
)
print(f"Sale created: {new_sale}")
print(f"Updated stock: {new_product.quantity_in_stock}")

new_balance = calculate_balance()
print(f"\nNew Balance: R$ {new_balance:.2f}")

if initial_balance == new_balance:
    print("RESULT: Balance did NOT update.")
else:
    profit_diff = new_balance - initial_balance
    print(f"RESULT: Balance updated. Profit difference: R$ {profit_diff:.2f}")
    print(f"Expected profit: R$ {(150.00 - 100.00) * 3:.2f}")

# Cleanup
print("\nCleaning up...")
new_sale.delete()
new_product.delete()
print("--- End Verification ---")
