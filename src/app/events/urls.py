from django.urls import include, path

from events.views import EventResults, EventDetail, ApplicationCreate

urlpatterns = [
    path('<int:pk>/', EventDetail.as_view(), name='event_detail'),
    path('<int:pk>/results/', EventResults.as_view(), name='event_detail'),
    path('<int:pk>/hx-payment-info/', EventDetail.hx_get_payment_info, name='hx_event_payment_info'),
    path('<int:pk>/application/create/', ApplicationCreate.as_view(), name="application_create"),
    ]