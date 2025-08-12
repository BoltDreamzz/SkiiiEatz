from django.contrib import admin
from .models import Avatar, UserProfile, User

admin.site.register(Avatar)
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'avatar')
    search_fields = ('user__email', 'user__full_name')
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'city', 'is_vendor', 'is_delivery_agent', 'is_active', 'is_staff')
    search_fields = ('email', 'full_name')
    list_filter = ('is_vendor', 'is_delivery_agent', 'is_active', 'is_staff')
    ordering = ('email',)
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('userprofile')

