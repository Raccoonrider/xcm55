from django.contrib import admin

from sponsors.models import Sponsor, EventSponsor

@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["name"]}
    model=Sponsor
    search_fields = ('name', )
    list_display = ('name', 'phone_number', 'active')
    list_filter = ('active',)
    ordering = ('-active', 'name')

@admin.register(EventSponsor)
class EventSponsorModelAdmin(admin.ModelAdmin):
    model = EventSponsor
    list_display = ('__str__', 'event', 'sponsor', 'active')
    list_filter = ('active', 'event')
    ordering = ('-active', '-event__date')
    autocomplete_fields = ('sponsor',)

