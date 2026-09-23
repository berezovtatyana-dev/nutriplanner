from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .models import Product
from .utils import MealPlanSession
from django.contrib import messages

def product_list(request):
    products = Product.objects.all()
    return render(request, 
    'meals/product_list.html',
    {'products':products})

@require_POST
def add_to_plan(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        weight = int(request.POST.get('weight', 100))
        if weight <= 0:
            raise ValueError()
    except ValueError as e:
        messages.error(request, 'Некорректный id')
        return redirect('product_list')
    meal_plan = MealPlanSession(request)
    meal_plan.add_or_update(product.id, weight)
    messages.success(request, f'Продукт {product.name} добавлен')

    return redirect('product_list')