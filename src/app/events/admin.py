from django.contrib import admin

from events.models import *

class BaseModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["name"]}

@admin.register(Series)
class SeriesModelAdmin(BaseModelAdmin):
    model = Series
    search_fields = ('name',)
    list_display = ('__str__', 'active')
    list_filter = ('active', )
    ordering = ('-active', 'name')

@admin.register(Event)
class EventModelAdmin(BaseModelAdmin):
    model = Event
    search_fields = ('name', 'date', 'series')
    list_display = ('__str__', 'date', 'time', 'series', 'finished', 'active')
    list_filter = ('active', 'series')
    ordering = ('-active', 'finished', '-date')
    autocomplete_fields = ('series',)


@admin.register(Route)
class RouteModelAdmin(BaseModelAdmin):
    model = Route
    search_fields = ('name', 'series')
    list_display = ('__str__', 'series', 'active')
    list_filter = ('active',)
    ordering = ('-active', 'name')
    autocomplete_fields = ('series',)

@admin.register(Result)
class ResultModelAdmin(admin.ModelAdmin):
    model = Result
    search_fields = ('user_profile',)
    list_display = ('event', 'route', 'user_profile', 'time')


@admin.register(Application)
class ApplicationModelAdmin(admin.ModelAdmin):
    model = Application
    search_fields = ('user_profile', 'event')
    list_display = ('user_profile', 'event', 'route', 'created')
    autocomplete_fields = ('event', 'route', 'user_profile', 'result')


@admin.register(EventRoute)
class EventRouteModelAdmin(admin.ModelAdmin):
    model = EventRoute
    list_display = ('__str__', 'event', 'route', 'active')
    list_filter = ('active', 'event')
    ordering = ('-active', '-event__date')
    autocomplete_fields = ('event', 'route',)

