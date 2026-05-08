# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-12-25

### 🎉 Major Release - Quantity-Based Inventory System

This is a **major breaking release** that fundamentally changes how inventory is tracked in the system.

### ⚠️ Breaking Changes

- **Removed** `status` field from Product model (replaced with quantity tracking)
- **Removed** `quantity` field from Product model (replaced with `quantity_total`)
- **Changed** inventory logic from status-based (IN_STOCK/SOLD) to quantity-based tracking
- **Added** new `Sale` model to track individual sales transactions

### ✨ Added

- **New Field**: `quantity_total` - Tracks total quantity purchased
- **New Property**: `quantity_sold` - Automatically calculated from Sale records
- **New Property**: `quantity_in_stock` - Automatically calculated (total - sold)
- **New Property**: `is_sold_out` - Returns true when stock is depleted
- **New Model**: `Sale` - Tracks individual sales with quantity and price
- **New Form**: `SaleForm` - Form for recording product sales
- **New View**: `sell_product_view` - Handles the selling process
- **Stock Validation**: Prevents overselling with form and view-level validation

### 🔄 Changed

- Product model now supports multiple units of the same product
- Admin interface updated to display quantity fields instead of status
- Product list view now shows: quantity_total, quantity_sold, quantity_in_stock
- Balance calculation now based on Sale records instead of product status
- Seed script (`seed_products.py`) now creates products with random sales
- Verification script (`verify_balance.py`) updated to test Sale-based calculations

### 🔧 Fixed

- Django Admin error with non-existent fields in `list_display`
- Balance calculation now accurately reflects actual sales
- Stock count now based on actual inventory levels

### 📝 Migration Guide

#### For Existing Users (v1.x → v2.0.0)

1. **Backup your database** (CRITICAL!)
   ```bash
   # For SQLite
   copy db.sqlite3 db.sqlite3.backup
   ```

2. **Run the migration script**
   ```bash
   python migrate_v1_to_v2.py
   ```

3. **Apply Django migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Test thoroughly**
   - Verify product quantities are correct
   - Test the sell product flow
   - Check balance calculations

#### What Changes in Your Workflow

**Before (v1.x):**
- Each product had a status: IN_STOCK or SOLD
- Multiple units = multiple product records

**After (v2.0.0):**
- One product record per item type
- Track quantity: total purchased, sold, in stock
- Sales are separate records linked to products

### 🧪 Testing

All tests updated for v2:
- `tests_pagination.py` - Updated to use `quantity_total`
- Seed and verification scripts updated

### 📚 Documentation

- Added migration script: `migrate_v1_to_v2.py`
- Updated this CHANGELOG with migration guide

---

## [1.0.0] - 2025-12-XX

### Initial Release

- Basic inventory management system
- Status-based tracking (IN_STOCK/SOLD)
- Product categories
- User authentication
- Admin interface
- Pagination support
