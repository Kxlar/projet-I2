from django import forms

from .models import Character


class EquipForm(forms.ModelForm):

    class Meta:
        model = Character
        fields = ("lieu",)
    