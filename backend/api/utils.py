from recipes.models import Recipe, RecipeIngredient


def get_shopping_cart(user):
    recipes = Recipe.objects.filter(shoppinglist__user=user)
    ingredients = RecipeIngredient.objects.filter(recipe__in=recipes).all()
    shopping_cart = {}
    m_units = {}
    for ingredient in ingredients:
        name = ingredient.ingredient.name
        amount = ingredient.amount
        if name in shopping_cart:
            shopping_cart[name] += amount
        else:
            shopping_cart[name] = amount
            m_units[name] = ingredient.ingredient.measurement_unit

    return shopping_cart, m_units
