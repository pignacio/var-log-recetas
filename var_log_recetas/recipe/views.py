from django.shortcuts import render
from .forms import RecipeAddForm, MeasuredIngredientForm



def home(request):
    return render(request, 'recipe/home.html', {
        'recipes': Recipe.objects.all().order_by('id'),
    })


def recipe_show(request, recipe_id):
    pass


def recipe_add(request):
    recipe = Recipe()
    if request.method == "POST":
        form = RecipeAddForm(request.POST, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('recipe_recipe_edit', recipe.id)
    else:
        form = RecipeAddForm(instance=recipe)
    return render(request, 'recipe/recipe_add.html', {
        'form': form,
    })
