from django.contrib.admin import SimpleListFilter
from datetime import date

class ChainedPrepopulatedFieldsMixin:
    chained_prepopulated_fields = tuple()

    def get_prepopulated_field_key(self, field):
        model_name = self.model.__class__.__name__
        return f'{model_name}-adminform-{field}'


    def save_form(self, request, form, change:bool):

        for field in self.chained_prepopulated_fields:
            request.session[self.get_prepopulated_field_key(field)] = form.data.get(field)
        
        return super().save_form(request, form, change)


    def get_form(self, request, obj = ..., change = ..., **kwargs):
        form = super().get_form(request, obj, change, **kwargs)


        for field in self.chained_prepopulated_fields:
            value = request.session.get(self.get_prepopulated_field_key(field))
            if value:
                form.base_fields[field].initial = value

        return form
    
class DateFilter(SimpleListFilter):
    title = "Дата"
    parameter_name = 'date'

    def lookups(self, request, model_admin):
        return (("future", "Будущие"), ("today", "Сегодня"), ("past", "Прошедшие"))


    def queryset(self, request, queryset):
        if self.value() == "future":
            return queryset.filter(date__gt=date.today())
        if self.value() == "today":
            return queryset.filter(date=date.today())
        if self.value() == "past":
            return queryset.filter(date__lt=date.today())
        return queryset.all()