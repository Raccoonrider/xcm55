from django.urls import include, path

from events.views import EventDetail, ApplicationCreate

urlpatterns = [
    path('<int:pk>/', EventDetail.as_view(), name='event_detail'),
    path('<int:pk>/application/create/', ApplicationCreate.as_view(), name="application_create"),
    ]