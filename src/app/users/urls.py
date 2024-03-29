from django.urls import include, path

from users.views import UserProfileCreateUpdate

urlpatterns = [
    path('create/', UserProfileCreateUpdate.as_view(), name="user_profile_create"),
    path('update/', UserProfileCreateUpdate.as_view(), name="user_profile_update"),
    ]