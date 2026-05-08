"""
Data Migration Script: v1 to v2
================================

This script migrates data from the old status-based system (v1) to the new 
quantity-based system with sales tracking (v2).

IMPORTANT: Make a backup of your database before running this script!

What this script does:
1. For each product with old 'status' field:
   - If status was 'IN_STOCK': Sets quantity_total to old quantity value
   - If status was 'SOLD': Creates a Sale record and sets quantity_total
2. Removes old status and quantity fields (handled by Django migrations)

Usage:
    python migrate_v1_to_v2.py
"""

import os
import django
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'revenda_estoque.settings')
django.setup()

from api.models import Product, Sale
from django.db import transaction

def migrate_data():
    print("=" * 60)
    print("Data Migration: v1.x → v2.0.0")
    print("=" * 60)
    print("\nWARNING: This will modify your database!")
    print("Make sure you have a backup before proceeding.\n")
    
    response = input("Do you want to continue? (yes/no): ")
    if response.lower() != 'yes':
        print("Migration cancelled.")
        return
    
    print("\nStarting migration...\n")
    
    # Note: This script assumes you're running it BEFORE the migration
    # that removes the old fields. If the fields are already removed,
    # you'll need to restore from backup or manually set quantity_total.
    
    migrated_count = 0
    sales_created = 0
    
    with transaction.atomic():
        products = Product.objects.all()
        total_products = products.count()
        
        print(f"Found {total_products} products to migrate.\n")
        
        for product in products:
            # Check if product has old 'status' field
            # If migrations already ran, this won't work
            try:
                old_status = getattr(product, 'status', None)
                old_quantity = getattr(product, 'quantity', 1)
            except AttributeError:
                print("⚠️  Old fields (status/quantity) not found.")
                print("   Migration may have already been applied.")
                print("   Please restore from backup if needed.")
                return
            
            # Set quantity_total based on old quantity
            if not hasattr(product, 'quantity_total') or product.quantity_total == 0:
                product.quantity_total = old_quantity
            
            # If product was marked as SOLD, create a Sale record
            if old_status == 'SOLD':
                Sale.objects.create(
                    product=product,
                    quantity=old_quantity,
                    price_sold=product.sale_value or product.cost
                )
                sales_created += 1
                print(f"✓ Migrated SOLD product: {product.name}")
            else:
                print(f"✓ Migrated IN_STOCK product: {product.name}")
            
            product.save()
            migrated_count += 1
    
    print("\n" + "=" * 60)
    print("Migration Complete!")
    print("=" * 60)
    print(f"Products migrated: {migrated_count}")
    print(f"Sales records created: {sales_created}")
    print("\nNext steps:")
    print("1. Run: python manage.py makemigrations")
    print("2. Run: python manage.py migrate")
    print("3. Test your application thoroughly")
    print("=" * 60)

if __name__ == "__main__":
    migrate_data()
