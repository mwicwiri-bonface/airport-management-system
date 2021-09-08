from admin_interface.models import Theme
from django.contrib import admin, messages
from django.utils.translation import ngettext
from django.contrib.auth.models import Group
from .models import Attendant, AttendantProfile, AttendantFeedback


class AttendantAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'username')
    search_fields = ('first_name', 'last_name', 'email', 'username',)
    list_filter = ('is_active', 'is_archived', 'updated', 'created')

    actions = ['make_active', 'make_inactive']

    def make_active(self, request, queryset):
        updated = queryset.update(is_active=True, is_archived=False)
        self.message_user(request, ngettext(
            '%d Attendant has successfully been marked as active.',
            '%d Attendants have been successfully marked as active.',
            updated,
        ) % updated, messages.SUCCESS)

    make_active.short_description = "Approve Attendant"

    def make_inactive(self, request, queryset):
        updated = queryset.update(is_archived=True)
        self.message_user(request, ngettext(
            '%d Attendant has been archived successfully.',
            '%d Attendants have been archived successfully.',
            updated,
        ) % updated, messages.INFO)

    make_inactive.short_description = "Archive Attendant"

    def has_delete_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return True


class AttendantProfileAdmin(admin.ModelAdmin):
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


class AttendantFeedbackAdmin(admin.ModelAdmin):
    list_display = ('subject', 'message', 'created')
    list_filter = ('created',)
    search_fields = ('subject', 'message',)

    def has_delete_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return True


admin.sites.AdminSite.site_header = 'Airport admin header'
admin.sites.AdminSite.site_title = 'Airport admin title'
admin.sites.AdminSite.index_title = 'Airport admin index'
admin.site.unregister(Group)
# admin.site.unregister(Theme)
admin.site.register(Attendant, AttendantAdmin)
admin.site.register(AttendantProfile, AttendantProfileAdmin)
admin.site.register(AttendantFeedback, AttendantFeedbackAdmin)
