from django.contrib import admin
from .models import Vendor, Business, CommissionSetting, Earning, PayoutRequest

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'user', 'is_approved', 'created_at')
    list_filter = ('is_approved',)
    actions = ['approve_vendors']

    def approve_vendors(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f"{updated} vendor(s) approved.")
    approve_vendors.short_description = "Approve selected vendors"

admin.site.register(Business)

admin.site.register(CommissionSetting)
admin.site.register(Earning)
admin.site.register(PayoutRequest)
