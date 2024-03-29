from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from events.models import Event, Route, EventRoute, Application


class ApplicationForm(forms.Form):
    route=forms.ModelChoiceField(
        queryset=Route.objects.all(),
        required=True,
        label="Дистанция",
        initial=1,
    )

    confirm_rules=forms.BooleanField(
        initial=False,
        required=True,
        label=f"Ознакомлен с положением и правилами мероприятия"
    )

    confirm_personal=forms.BooleanField(
        initial=False,
        required=True,
        label=f"Согласен на обработку персональных данных"
    )



