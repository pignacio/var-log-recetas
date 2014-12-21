from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, 'recipe/home.html', {
        'recipes': Recipe.objects.all().order_by('id'),
    })


def recipe_show(request, recipe_id):
    pass
