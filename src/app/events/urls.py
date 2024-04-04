from django.urls import include, path

from events.views import EventDetail, ApplicationCreate

urlpatterns = [
    path('<int:pk>/application/create/', ApplicationCreate.as_view(), name="application_create"),
    ]