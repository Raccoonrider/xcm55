from rest_framework import serializers

from users.models import (
    UserProfile
)

from events.models import (
    Event,
    Route,
    Application,
    Result,
    AgeGroup,
)

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        exclude = ('phone_number',)

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        depth = 1
        exclude = ('sponsors',)

class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = "__all__"

class ApplicationSerializer(serializers.ModelSerializer):
    user_profile = UserProfileSerializer

    class Meta:
        model = Application
        depth = 1
        fields = "__all__"

class ResultSerializer(serializers.ModelSerializer):
    user_profile = UserProfileSerializer

    class Meta:
        model = Result
        depth = 1
        fields = "__all__"

class AgeGroupSerializer(serializers.ModelSerializer):
    birthday_min = serializers.DateField()
    birthday_max = serializers.DateField()
    class Meta:
        model = AgeGroup
        fields = "__all__"
