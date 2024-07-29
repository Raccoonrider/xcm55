from datetime import date

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import FormView
from django.views import View
from django.conf import settings
from django.urls import reverse
from django.db.models import F

from common.enums import ResultStatus, Category, Gender
from events.models import Event, Application, PaymentWindow, AgeGroup, Result
from events.forms import ApplicationForm
from sponsors.models import Referral

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

        self.request.session['ref_uuid'] = self.request.GET.get('ref_uuid')

        elites = (Application.objects
            .filter(event=event, category=Category.Elite)
            .order_by('created')
            )
        route_marathon, route_halfmarathon = event.routes.all().order_by('-distance')

        agegroups = AgeGroup.objects.filter(event=event).order_by('gender', 'age_max')
        if agegroups:
            amateurs_marathon = zip(agegroups, [
                (Application.objects
                    .filter(event=event, category=Category.Default, route=route_marathon)
                    .filter(user_profile__birthday__gte=ag.birthday_min())
                    .filter(user_profile__birthday__lte=ag.birthday_max())
                    .filter(user_profile__gender=ag.gender)
                    .order_by('user_profile__last_name'))
                for ag in agegroups]
            )
        else:     
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
            or event.finished == True
            or event.registration_closed == True
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
            'agegroups': agegroups,
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
        if self.event.finished or self.event.registration_closed:
            return HttpResponseRedirect('/')
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
        application.referral = Referral.from_uuid(self.request.session.get('ref_uuid'))
        application.save()
        return HttpResponseRedirect(self.event.get_absolute_url() + "#payment_info")

class EventResults(View):
    template_name = "events/results.html"

    def get(self, *args, pk=None, **kwargs):
        if pk is not None:
            event = get_object_or_404(Event, pk=pk)
        else:
            event = (Event.objects
                .filter(active=True, finished=False)
                .order_by('-date')
                .first()
                )
        
        if self.request.user.is_authenticated and self.request.user.profile:
            my_application = (Application.objects
                .filter(event=event, user_profile=self.request.user.profile)
                .first()
                )
            my_result = my_application.result
        else:
            my_result = None

        results = {}
        for result in Result.objects.filter(event=event, active=True).order_by('status', F('time').asc(nulls_last=True),):
            key = result.render_category()
            results[key] = results.get(key) or []
            results[key].append(result)

        results = sorted(results.items(), key=lambda x: (x[0] != "Элита", x[0] == "Полумарафон", x[0] == "Юниоры", x[0]))
               
        context = {
            'event': event,
            'my_result': my_result,
            'results': results,
        }
        return render(request=self.request, template_name=self.template_name, context=context)