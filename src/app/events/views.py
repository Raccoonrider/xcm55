from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import FormView
from django.views import View
from django.conf import settings
from django.urls import reverse

from common.enums import ResultStatus, Category, Gender
from events.models import Event, Application
from events.forms import ApplicationForm

class EventDetail(View):
    template_name = "events/detail.html"
    model = Event

    def get(self, *args, pk=None, **kwargs):
        if pk is not None:
            instance = get_object_or_404(self.model, pk=pk)
        else:
            instance = (self.model.objects
                .filter(active=True, finished=False)
                .order_by('-date')
                .first()
                )
        if self.request.user.is_authenticated and self.request.user.profile:
            my_application = (Application.objects
                .filter(event=instance, user_profile=self.request.user.profile)
                .first()
                )
        else:
            my_application = None

        elites = (Application.objects
            .filter(event=instance, category=Category.Elite)
            .order_by('created')
            )
        amateurs = (Application.objects
            .filter(event=instance, category=Category.Default)
            .order_by('created')
            )
        routes = instance.routes.all().order_by('-distance')

        registration_disabled = bool(my_application)

        context = {
            'event': instance,
            'my_application': my_application,
            'registration_disabled': registration_disabled,
            'elites': elites,
            'amateurs': amateurs,
            'marathon': routes[0],
            'halfmarathon': routes[1],
        }
        return render(request=self.request, template_name=self.template_name, context=context)
    
    @classmethod
    def hx_get_payment_info(cls, *args, pk=None, **kwargs):
        instance = get_object_or_404(cls.model, pk=pk)
        return HttpResponse(instance.payment_info, content_type='text/plain')

class ApplicationCreate(FormView):
    template_name = "events/application.html"
    form_class = ApplicationForm

    def redirect_user(self):
        self.request.session['redirect'] = self.request.path
        if self.request.user.is_authenticated == False:
            return HttpResponseRedirect(settings.LOGIN_URL)
        if self.request.user.profile is None:
            return HttpResponseRedirect(reverse('user_profile_create'))
        
        application = Application.objects.filter(
            event=self.event, 
            user_profile=self.request.user.profile)
        if application:
            return HttpResponseRedirect('/')

    def get(self, *args, pk:int=None, **kwargs):
        self.event = Event.objects.get(pk=pk)
        return self.redirect_user() or super().get(*args, **kwargs)
    
    def post(self, *args, pk:int=None, **kwargs):
        self.event = Event.objects.get(pk=pk)
        return self.redirect_user() or super().post(*args, **kwargs)

    def get_form(self, form_class=ApplicationForm) -> ApplicationForm:
        form = super().get_form(form_class)
        qs = self.event.routes.all().order_by('-distance')
        form.fields['route'].queryset = qs
        return form

    def form_valid(self, form) -> HttpResponse:
        application = Application()
        application.event = self.event
        application.route = form.cleaned_data['route']
        application.helmet_not_needed = form.cleaned_data['helmet_not_needed']
        application.user_profile = self.request.user.profile
        application.category = form.cleaned_data['category']
        application.save()
        return HttpResponseRedirect(self.event.get_absolute_url())
