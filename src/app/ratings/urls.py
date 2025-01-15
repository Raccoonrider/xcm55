from django.urls import include, path

import ratings.views

urlpatterns = [
    path('<int:year>/', ratings.views.rating, name='rating_detail'),
    ]