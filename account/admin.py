

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile

# Inline model to attach UserProfile to User in admin
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False  # Don't allow deleting from inline
    verbose_name_plural = 'Profile'

# Extend UserAdmin to include UserProfile
class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_role', 'is_staff')

    def get_role(self, obj):
        return obj.userprofile.role if hasattr(obj, 'userprofile') else '-'
    get_role.short_description = 'Role'

# Unregister default User admin and register our custom version
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
