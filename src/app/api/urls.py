from django.urls import path, include

import api.views

urlpatterns = [
        path('events/', api.views.EventListAPIView.as_view()),
        path('events/<int:pk>/', api.views.EventDetailAPIView.as_view()),
        path('events/<int:event__pk>/age_groups/', api.views.AgeGroupListAPIView.as_view()),
        path('events/<int:event__pk>/applications/', api.views.ApplicationListAPIView.as_view()),
        path('events/<int:event__pk>/results/', api.views.ResultListAPIView.as_view()),
    ]   