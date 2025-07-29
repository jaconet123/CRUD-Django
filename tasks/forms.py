from django.forms import ModelForm
from .models import Task

class createtaskform(ModelForm):
    class Meta:
        model= Task
        fields=['title','description','important']