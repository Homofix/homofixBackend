from django import forms
from django.forms import formset_factory
from .models import SubCategory

class CategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = '__all__'
