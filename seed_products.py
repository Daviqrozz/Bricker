import os
import django
import random
import decimal

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'revenda_estoque.settings')
django.setup()

from api.models import Product, Category, Sale

def create_products():
    print("Creating test products (v2.0.0)...")
    
    # Ensure a category exists
    category, created = Category.objects.get_or_create(name="Teste Geral")
    
    adjectives = ["Novo", "Usado", "Premium", "Básico", "Luxo", "Antigo", "Moderno"]
    nouns = ["Camisa", "Calça", "Tênis", "Boné", "Relógio", "Óculos", "Mochila", "Jaqueta"]
    
    for i in range(20):
        name = f"{random.choice(nouns)} {random.choice(adjectives)} {random.randint(100, 999)}"
        cost = decimal.Decimal(random.randrange(10, 200))
        sale_value = cost * decimal.Decimal(random.uniform(1.2, 2.0))
        quantity_total = random.randint(5, 50)
        
        product = Product.objects.create(
            name=name,
            category=category,
            quantity_total=quantity_total,
            cost=cost,
            sale_value=sale_value,
            observation="Gerado automaticamente para teste"
        )
        
        # Randomly create some sales for this product (0 to 3 sales)
        num_sales = random.randint(0, 3)
        for _ in range(num_sales):
            # Ensure we don't oversell
            if product.quantity_in_stock > 0:
                quantity_to_sell = random.randint(1, min(5, product.quantity_in_stock))
                Sale.objects.create(
                    product=product,
                    quantity=quantity_to_sell,
                    price_sold=sale_value
                )
        
        print(f"Created: {product.name} | Total: {product.quantity_total} | Sold: {product.quantity_sold} | Stock: {product.quantity_in_stock}")

    print(f"\nSuccessfully created 20 products with random sales.")

if __name__ == "__main__":
    create_products()
