from django.shortcuts import render, get_object_or_404,redirect
from .models import Product, Category, Sale
from .forms import ProductForm, CategoryForm, SaleForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Sum, F
from django.utils import timezone
from datetime import timedelta
from django.http import JsonResponse
from django_multitenant.utils import set_current_tenant

@login_required
def product_view(request):
  set_current_tenant(request.user)

  products = Product.objects.all()

  # Date Filtering
  period = request.GET.get('period', '30')
  period_label = "Últimos 30 dias"

  start_date = None

  if period == 'all':
    period_label = "Todo o período"
  else:
    try:
      days = int(period)
      start_date = timezone.now() - timedelta(days=days)

      if days == 90:
        period_label = "Últimos 3 meses"
      elif days == 180:
        period_label = "Últimos 6 meses"
      elif days == 365:
        period_label = "Último ano"
      else:
        period_label = f"Últimos {days} dias"
    except ValueError:
      # Default to 30 days if invalid
      start_date = timezone.now() - timedelta(days=30)
      period = '30'

  # Recent Sales Filtering
  if start_date:
    recent_sales = Sale.objects.filter(created_at__gte=start_date)

    relevant_products = Product.objects.filter(created_at__gte=start_date)
    total_spent = relevant_products.aggregate(total=Sum(F('cost') * F('quantity_total')))['total'] or 0
    new_products_count = relevant_products.count()
  else:
    recent_sales = Sale.objects.all()
    relevant_products = Product.objects.all()
    total_spent = Product.objects.aggregate(total=Sum(F('cost') * F('quantity_total')))['total'] or 0
    new_products_count = relevant_products.count()

  total_sales = recent_sales.aggregate(total=Sum('price_sold'))['total'] or 0

  # Calculate total cost for sold items in this period
  total_cost = 0
  for sale in recent_sales:
    total_cost += sale.product.cost * sale.quantity

  last_month_balance = total_sales - total_cost

  # Count products with stock available
  stock_count = sum(1 for p in Product.objects.all() if p.quantity_in_stock > 0)

  # Pagination
  page = request.GET.get('page', 1)
  per_page = request.GET.get('per_page', 10)  # Default 10 products per page

  # Validate per_page value
  try:
    per_page = int(per_page)
    if per_page not in [10, 25, 50, 100]:
      per_page = 10
  except (ValueError, TypeError):
    per_page = 10

  paginator = Paginator(products, per_page)

  try:
    products = paginator.page(page)
  except PageNotAnInteger:
    products = paginator.page(1)
  except EmptyPage:
    products = paginator.page(paginator.num_pages)

  # Calculate Gross Income (Profit + Investment)
  gross_income = last_month_balance + total_spent

  show_onboarding = False
  if request.user.is_authenticated:
    user_profile = getattr(request.user, 'profile', None)

    if user_profile and user_profile.onboarding_completed_at is None:
      if not request.session.get('onboarding_viewed'):
        show_onboarding = True
        request.session['onboarding_viewed'] = True

  onboarding_completed = request.user.profile.onboarding_completed_at is not None

  context = {
    'products_list': products,
    'new_products_count': new_products_count,
    'last_month_balance': last_month_balance,
    'stock_count': stock_count,
    'per_page': per_page,
    'total_spent': total_spent,
    'gross_income': gross_income,
    'period': period,
    'period_label': period_label,
    'show_onboarding': show_onboarding,
    'onboarding_completed': onboarding_completed
  }

  return render(request, 'views/products.html', context)

@login_required
def create_view(request):
  if request.method == "POST":
    form = ProductForm(request.POST)

    if form.is_valid():
      product = form.save(commit=False)
      product.user = request.user
      product.save()

      return redirect('products_view')

  form = ProductForm()
  form_category = CategoryForm()

  context = {
    'form':form,
    'form_category':form_category
  }

  return render(request, 'views/create.html', context)

@login_required
def create_category_view(request):
    if request.method == "POST":
        form_category = CategoryForm(request.POST)
        next_url = request.POST.get('next')

        print("Valor recebido para NEXT:", next_url)

        print("Dados completos do POST:", request.POST)

        if form_category.is_valid():
            form_category.save()

            if next_url:

                print(f"Redirecionando com sucesso para: {next_url}")
                return redirect(next_url)

            return redirect('products_view')

    return redirect('products_view')

@login_required
def edit_view(request, id):
  product = get_object_or_404(Product, pk=id, user=request.user)

  if request.method == 'POST':
    form = ProductForm(request.POST, instance=product)

    if form.is_valid():
      form.save()
      return redirect('products_view')
  else:
    form = ProductForm(instance=product)

  context = {
    'form': form,
    'product': product,
  }

  return render(request, 'views/edit.html', context)

@login_required
def delete_view(request, id):
    product = get_object_or_404(Product,pk=id)

    if request.method == 'POST':
        product.delete()
        return redirect('products_view')

    return redirect('products_view')

@login_required
def sell_product_view(request, id):
  product = get_object_or_404(Product, pk=id, user=request.user)

  if request.method == 'POST':
    form = SaleForm(request.POST, user=request.user)

    if form.is_valid():
      sale = form.save(commit=False)

      sale.user = request.user
      sale.product = product

      # Double-check stock availability
      if sale.quantity > product.quantity_in_stock:
        form.add_error('quantity', f'Quantidade indisponível. Estoque atual: {product.quantity_in_stock}')
      else:
        sale.save()
        return redirect('products_view')
  else:
    # Pre-fill the form with the selected product
    form = SaleForm(initial={
      'product': product,
      'price_sold': product.sale_value,
      'quantity': 1
    })

  context = {
    'form': form,
    'product': product,
  }

  return render(request, 'views/sell.html', context)

@login_required
def update_onboarding_preference(request):
  preference = request.GET.get('preference')
  profile = request.user.profile

  if preference == '1':
    profile.onboarding_completed_at = timezone.now()
  else:
    profile.onboarding_completed_at = None

  profile.save()
  return JsonResponse({'status': 'ok'})
