from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .models import Product
from .utils import MealPlanSession
from django.contrib import messages

def product_list(request):
    query = request.GET.get('q', '').strip()
    products = Product.objects.all()
    if query:
        q = query.lower()
        products = [p for p in products if q in p.name.lower()]
    return render(request,
        'meals/product_list.html',
        {'products': products, 'query': query})

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

def meal_plan_detail(request):
    meal_plan = MealPlanSession(request)
    items, totals = meal_plan.get_items_and_totals()
    context = {
        'items': items,
        'totals': totals
    }
    return render(request, 'meals/meal_plan.html', context)

@require_POST
def remove_from_plan(request, product_id):
    meal_plan = MealPlanSession(request)
    meal_plan.remove(product_id)
    messages.info(request, 'Продукт удален из вашего рациона')
    return redirect('meal_detail_plan')

@require_POST
def clear_plan(request):
    meal_plan = MealPlanSession(request)
    meal_plan.clear()
    messages.info(request, 'Ваш рацион полностью очищен')
    return redirect('meal_detail_plan')
