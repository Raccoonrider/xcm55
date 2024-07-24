from django.urls import path, include

import api.views

urlpatterns = [
        path('events/', api.views.EventListAPIView.as_view()),
        path('events/<int:pk>/', api.views.EventDetailAPIView.as_view()),
        path('events/<int:event__pk>/age_groups/', api.views.AgeGroupListAPIView.as_view()),
        path('routes/', api.views.RouteDetailAPIView.as_view()),
        path('routes/<int:pk>/', api.views.RouteDetailAPIView.as_view()),
        path('applications/', api.views.ApplicationDetailAPIView.as_view()),
        path('applications/<int:pk>/', api.views.ApplicationDetailAPIView.as_view()),
        path('results/', api.views.ResultDetailAPIView.as_view()),
        path('results/<int:pk>/', api.views.ResultDetailAPIView.as_view()),
    ]   