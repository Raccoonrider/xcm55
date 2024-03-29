from django.urls import include, path

from events.views import ApplicationCreate

urlpatterns = [
    path('<int:event_pk>/application/create/', ApplicationCreate.as_view(), name="application_create"),
    ]