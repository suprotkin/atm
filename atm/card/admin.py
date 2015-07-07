from django.contrib import admin

from . import models


class CardAdmin(admin.ModelAdmin):
    list_display = ('__str__', '_balance', 'is_locked', 'try_count')
    list_filter = ('is_locked',)

admin.site.register(models.Card, CardAdmin)


class OperationLogAdmin(admin.ModelAdmin):
    list_display = ('card', 'time', 'code', 'amount')
    list_display_links = ('time',)
    list_filter = ('card', 'code')

admin.site.register(models.Operation, OperationLogAdmin)
