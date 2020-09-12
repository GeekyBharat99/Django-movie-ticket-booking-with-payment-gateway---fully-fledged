from django import forms
from .models import *

class Add_Movie_Form(forms. ModelForm):
    class Meta:
        model = Movies
        exclude = {"cat", "img2","img3", "img4", "trailer"}
        widgets = {
            "cat": forms.TextInput(attrs={"class": "form-control", "required": ""}),
            "title": forms.TextInput(attrs={"class": "form-control", "required": ""}),
            "r_date": forms.TextInput(attrs={"class": "form-control","required": ""}),
            "director": forms.TextInput(attrs={"class": "form-control", "required": ""}),
            "rate": forms.NumberInput(attrs={"class": "form-control", "required": ""}),
            "pro_house": forms.TextInput(attrs={"class": "form-control" ,"required": ""}),
            "des": forms.TextInput(attrs={"class": "form-control", "required": ""}),
            "img1": forms.FileInput(attrs={"class": "form-control", "required": ""}),

        }