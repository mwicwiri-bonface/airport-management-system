from django.contrib import admin, messages
from django.utils.translation import ngettext

from .models import Security, SecurityProfile, SecurityFeedback


class SecurityAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'username')
    search_fields = ('first_name', 'last_name', 'email', 'username',)
    list_filter = ('is_active', 'is_archived', 'updated', 'created')

    actions = ['make_active', 'make_inactive']

    def make_active(self, request, queryset):
        updated = queryset.update(is_active=True, is_archived=False)
        self.message_user(request, ngettext(
            '%d Security has successfully been marked as active.',
            '%d Securitys have been successfully marked as active.',
            updated,
        ) % updated, messages.SUCCESS)

    make_active.short_description = "Approve Security"

    def make_inactive(self, request, queryset):
        updated = queryset.update(is_archived=True)
        self.message_user(request, ngettext(
            '%d Security has been archived successfully.',
            '%d Securitys have been archived successfully.',
            updated,
        ) % updated, messages.INFO)

    make_inactive.short_description = "Archive Security"

    def has_delete_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return True


class SecurityProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'image', 'gender', 'is_active', 'created', 'updated')
    list_filter = ('gender', 'is_active', 'updated', 'created')
    search_fields = ('phone_number',)
    actions = ['make_active', 'make_inactive']

    def make_active(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, ngettext(
            '%d Profile has been successfully marked as active.',
            '%d Profiles have been successfully marked as active.',
            updated,
        ) % updated, messages.SUCCESS)

    make_active.short_description = "Mark selected Profiles as active"

    def make_inactive(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, ngettext(
            '%d Profile has been successfully marked as inactive.',
            '%d Profiles has been successfully marked as inactive.',
            updated,
        ) % updated)

    make_inactive.short_description = "Mark selected Profiles as inactive"

    def has_delete_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return True


class SecurityFeedbackAdmin(admin.ModelAdmin):
    list_display = ('subject', 'message', 'created')
    list_filter = ('created',)
    search_fields = ('subject', 'message',)

    def has_delete_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return True


admin.site.register(Security, SecurityAdmin)
admin.site.register(SecurityProfile, SecurityProfileAdmin)
admin.site.register(SecurityFeedback, SecurityFeedbackAdmin)



