from django.urls import include, path

import ratings.views

urlpatterns = [
    path('<int:year>/', ratings.views.rating, name='rating_detail'),
    path('hx/', ratings.views.hx_ratings, name='hx_ratings'),
    ]