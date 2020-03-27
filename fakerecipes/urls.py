"""_the_ app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls import handler404
from fakerecipes import views



#handler404 = 'app.views.error_404'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    path('login/', views.log_in, name="login"),
    path('signup/', views.signup, name="signup"),
    path('logout/', views.log_out, name="logout"),
    path('recipe/', views.share_recipe, name='share recipe'),
    path('recipe/<int:recipe_id>/', views.get_recipe, name='get recipe'),
    re_path(r'^s3direct/', include('s3direct.urls')),

]
