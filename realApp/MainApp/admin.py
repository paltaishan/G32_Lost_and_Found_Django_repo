from django.contrib import admin
from .models import Item, ClaimRequest

class ItemAdmin(admin.ModelAdmin):
    list_display = ('item_id', 'title', 'status', 'category', 'location', 'date_reported', 'reported_by')
    list_filter = ('status', 'category', 'location', 'date_reported')
    search_fields = ('title', 'description', 'location')
    radio_fields = {'status': admin.VERTICAL}

class ClaimRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'item', 'claimant', 'status', 'requested_at')
    list_filter = ('status', 'requested_at')
    search_fields = ('item__title', 'claimant__username')

admin.site.register(Item, ItemAdmin)
admin.site.register(ClaimRequest, ClaimRequestAdmin)
