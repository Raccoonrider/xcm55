from django.contrib import admin

from events.models import Event, Route, Series


class BaseModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["name"]}

@admin.register(Event)
class EventModelAdmin(BaseModelAdmin):
    pass

@admin.register(Series)
class SeriesModelAdmin(BaseModelAdmin):
    pass

@admin.register(Route)
class RouteModelAdmin(BaseModelAdmin):
    pass