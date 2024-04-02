from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.edit import FormView

from events.models import Event, Application
from events.forms import ApplicationForm

class ApplicationCreate(FormView):
    template_name = "events/application.html"
    form_class = ApplicationForm

    def get(self, *args, event_pk:int=None, **kwargs):
        self.event_pk = event_pk
        return super().get(*args, **kwargs)
    
    def post(self, *args, event_pk:int=None, **kwargs):
        self.event_pk = event_pk
        return super().post(*args, **kwargs)

    def get_form(self, form_class=ApplicationForm) -> ApplicationForm:
        form = super().get_form(form_class)
        qs = Event.objects.get(pk=self.event_pk).routes.all().order_by('-distance')
        form.fields['route'].queryset = qs
        return form

    def form_valid(self, form) -> HttpResponse:
        print("valid")
        application = Application()
        application.event = Event.objects.get(pk=self.event_pk)
        application.route = form.cleaned_data['route']
        application.helmet_not_needed = form.cleaned_data['helmet_not_needed']
        application.user_profile = self.request.user.profile
        application.save()
        return HttpResponseRedirect('/')
