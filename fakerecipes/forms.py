from django import forms
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from app.models import AppUser, Recipe, Ingredient

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=32, min_length=4, error_messages={'invalid': 'min 4, max 32'})
    password = forms.CharField(widget=forms.widgets.PasswordInput, label='Password')

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'image', 'description', 'difficulty', 'ingredients']
    


class UserCreationForm(forms.ModelForm):
    
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    username = forms.CharField(label='Username', max_length=32)
    email = forms.CharField(label='Email', widget=forms.EmailInput)
    name = forms.CharField(label='Name', max_length=32)

    class Meta:
        model = AppUser
        fields = ('username', 'email', 'name')

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = AppUser
        fields = ('username', 'email', 'password', 'is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]