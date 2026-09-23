# логика работы с сессиями
from .models import Product

SESSION_KEY = 'meal_plan'

class MealPlanSession:
    def __init__(self, request):
        self.session = request.session
        meal_plan = self.session.get(SESSION_KEY)

        if not meal_plan:
            meal_plan = self.session[SESSION_KEY] = {}

        self.meal_plan = meal_plan

    def add_or_update(self, product_id, weight):
        str_id = str(product_id)
        if weight > 0:
            if str_id in self.meal_plan:
                self.meal_plan[str_id] += weight
            else:
                self.meal_plan[str_id] = weight
            self.save()

    def remove(self, product_id):
        str_id = str(product_id)
        if str_id in self.meal_plan:
            del self.meal_plan[str_id]
            self.save()

    def clear(self):
        self.session[SESSION_KEY] = {}
        self.save()

    def save(self):
        self.session.modified = True

    def get_items_and_totals(self):
        product_ids = self.meal_plan.keys()
        products = Product.objects.filter(id__in=product_ids)
        items = []
        totals = {
            'calories': 0.0,
            'proteins': 0.0,
            'fats': 0.0,
            'carbs': 0.0,
        }
        for product in products:
            weight = self.meal_plan.get(str(product.id), 0)
            # коэффициент перерасчета т.к. в базе данных на 100 грамм
            factor = weight / 100.0

            i_calories = round(product.calories * factor, 1)
            i_proteins = round(product.proteins * factor, 1)
            i_fats = round(product.fats * factor, 1)
            i_carbs = round(product.carbs * factor, 1)
            items.append({
                'product': product,
                'weight': weight,
                'calories': i_calories,
                'proteins': i_proteins,
                'fats': i_fats,
                'carbs': i_carbs,
            })
            totals['calories'] += i_calories
            totals['proteins'] += i_proteins
            totals['fats'] += i_fats
            totals['carbs'] += i_carbs

        return items, totals
