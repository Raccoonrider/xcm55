from datetime import date

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import FormView
from django.views import View
from django.conf import settings
from django.urls import reverse

from common.enums import ResultStatus, Category, Gender
from events.models import Event, Application, PaymentWindow
from events.forms import ApplicationForm

class EventDetail(View):
    template_name = "events/detail.html"
    model = Event

    def get(self, *args, pk=None, **kwargs):
        if pk is not None:
            event = get_object_or_404(self.model, pk=pk)
        else:
            event = (self.model.objects
                .filter(active=True, finished=False)
                .order_by('-date')
                .first()
                )
        if self.request.user.is_authenticated and self.request.user.profile:
            my_application = (Application.objects
                .filter(event=event, user_profile=self.request.user.profile)
                .first()
                )
        else:
            my_application = None

        elites = (Application.objects
            .filter(event=event, category=Category.Elite)
            .order_by('created')
            )
        route_marathon, route_halfmarathon = event.routes.all().order_by('-distance')
        amateurs_marathon = (Application.objects
            .filter(event=event, category=Category.Default, route=route_marathon)
            .order_by('created')
            )
        amateurs_halfmarathon = (Application.objects
            .filter(event=event, category=Category.Default, route=route_halfmarathon)
            .order_by('created')
            )

        registration_disabled = (
            my_application is not None
            and event.finished == False
        )

        marathon_payment_windows = PaymentWindow.objects.filter(event=event, route=route_marathon)
        marathon_payment_windows_stale = marathon_payment_windows.filter(active_until__lt=date.today())
        marathon_payment_window_active = marathon_payment_windows.filter(active_until__gte=date.today()).first()
        marathon_payment_windows_next = marathon_payment_windows.filter(active_until__gte=date.today())[1:]

        halfmarathon_payment_windows = PaymentWindow.objects.filter(event=event, route=route_halfmarathon)
        halfmarathon_payment_windows_stale = halfmarathon_payment_windows.filter(active_until__lt=date.today())
        halfmarathon_payment_window_active = halfmarathon_payment_windows.filter(active_until__gte=date.today()).first()
        halfmarathon_payment_windows_next = halfmarathon_payment_windows.filter(active_until__gte=date.today())[1:]

        context = {
            'event': event,
            'my_application': my_application,
            'registration_disabled': registration_disabled,
            'elites': elites,
            'amateurs_marathon': amateurs_marathon,
            'amateurs_halfmarathon': amateurs_halfmarathon,
            'marathon': route_marathon,
            'halfmarathon': route_halfmarathon,
            'marathon_payment_windows_stale' : marathon_payment_windows_stale,
            'marathon_payment_window_active' : marathon_payment_window_active,
            'marathon_payment_windows_next' : marathon_payment_windows_next,
            'halfmarathon_payment_windows_stale' : halfmarathon_payment_windows_stale,
            'halfmarathon_payment_window_active' : halfmarathon_payment_window_active,
            'halfmarathon_payment_windows_next' : halfmarathon_payment_windows_next,
        }
        return render(request=self.request, template_name=self.template_name, context=context)
    
    @classmethod
    def hx_get_payment_info(cls, request, pk):
        if request.user.is_authenticated and request.user.profile:
            event = get_object_or_404(cls.model, pk=pk)
            my_application = (Application.objects
                .filter(event=event, user_profile=request.user.profile)
                .first()
                )
            payment_windows = PaymentWindow.objects.filter(event=event, route=my_application.route)
            payment_window_active = payment_windows.filter(active_until__gte=date.today()).first()
            
            context = {
                'event': event,
                'my_application': my_application,
                'payment_window_active' : payment_window_active,
            }
            return render(request=request, template_name='events/hx_payment_info.html', context=context)
        else:
            return HttpResponse("")

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
        return HttpResponseRedirect(self.event.get_absolute_url() + "#payment_info")
