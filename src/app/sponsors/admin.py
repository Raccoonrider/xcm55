from django.contrib import admin

from sponsors.models import Sponsor

@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    model=Sponsor
    search_fields = ('name', )
    list_display = ('name', 'phone_number', 'active')
    list_filter = ('active',)
    ordering = ('-active', 'name')
