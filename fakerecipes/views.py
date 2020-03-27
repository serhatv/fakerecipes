from django.http import HttpResponse, Http404, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.core.exceptions import ValidationError

from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required


from datetime import datetime


from fakerecipes.forms import LoginForm, RecipeForm
from fakerecipes.admin import UserCreationForm
from fakerecipes.models import AppUser, Recipe, Ingredient
from django.conf import settings

from django.db.models import Count

def index(req):
    recipes = Recipe.objects.all()

    # I couldnt find a way to get the Ingredient names so
    # I get them with a for loop... so shame...
    ingredients_annotated = Recipe.objects.all().values('ingredients').annotate(total=Count('ingredients')).order_by('-total')
    ingredients_with_total = []
    for i in ingredients_annotated:
        ingredient = Ingredient.objects.get(id=i['ingredients'])
        ingredients_with_total.append({'name': ingredient.name, 'total': i['total']})

    return render(req, 'index.html', {'recipes': recipes, 'ingredient_list': ingredients_with_total})


@login_required
def share_recipe(req):
    if req.method == 'GET':
        form = RecipeForm()
        return render(req, 'share_recipe.html', {'form': form})
    else:
        form = RecipeForm(req.POST, req.FILES)
        if form.is_valid():
            try:
                recipe = form.save(commit=False)
                user = AppUser.objects.get(id=req.user.id)
                recipe.created_by = user
                recipe.save()
                form.save_m2m()
                return redirect('/')
            except:
                return HttpResponse('Internal Server Error')

        else:
            return render(req, 'share_recipe.html', {'form': form})




def get_recipe(req, recipe_id):
    try:
        recipe = Recipe.objects.get(id=recipe_id)
    except:
        recipe = None

    return render(req, 'recipe.html', {'recipe': recipe})


# AUTH RELATED


@csrf_exempt
def log_in(req):
    if req.method == 'GET':
        if req.user.is_authenticated:
            return redirect('/')
        else:
            form = LoginForm()
            return render(req, 'login.html', {'form': form})
    else:
        form = LoginForm(req.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(req, username=username, password=password)

            if user is not None:
                login(req, user)
                return redirect('/')
            else:
                return render(req, 'login.html', {'form': form, 'err_msg': 'Invalid Credentials.'})
        else:
            return render(req, 'login.html', {'form': form})


@csrf_exempt
def signup(req):
    if req.method == 'GET':
        if req.user.is_authenticated:
            return redirect('/')
        else:
            form = UserCreationForm()
            return render(req, 'signup.html', {'form': form})
    else:
        form = UserCreationForm(req.POST)

        if form.is_valid():
            try:
                form.save()
                return redirect('/login')
            except ValidationError:
                return render(req, 'signup.html', {'form': form, 'err_msg': 'An Error Occured...'})
        else:
            return render(req, 'signup.html', {'form': form, 'err_msg': 'Invalid fields.'})

def log_out(request):
    logout(request)
    return redirect('/')



def error_404(req, exc):
    return HttpResponse('404')

