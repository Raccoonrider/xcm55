from django.urls import include, path

from events.views import *

urlpatterns = [
    path('<int:pk>/', EventDetail.as_view(), name='event_detail'),
    path('<int:pk>/rules/', EventDetail.as_view(rules=True), name='event_rules'),
    path('<int:pk>/results/', EventResults.as_view(), name='event_results'),
    path('<int:pk>/org-tools/list/by_number/', organizer_list, kwargs={'order': 'number'}),
    path('<int:pk>/org-tools/list/by_name/', organizer_list, kwargs={'order': 'user_profile__last_name'}),
    path('<int:pk>/application/create/', ApplicationCreate.as_view(), name="application_create"),
    path('order/<int:application_id>/success/', ApplicationCreate.success, name="application_success"),
    path('order/failure/', render, kwargs={'template_name': 'events/application_failure.html'}, name="application_failure"),
    path('hx-calendar/', EventDetail.hx_calendar, name='hx_calendar'),
    path('hx-results/', EventDetail.hx_results, name='hx_results'),
    path('bundle/<int:pk>/application/create/', BundleApplicationCreate.as_view(), name="bundle_application_create"),
    ]