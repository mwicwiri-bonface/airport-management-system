from django.contrib import admin, messages
from django.utils.translation import ngettext
from .models import Profile, Feedback
from django.contrib.auth import get_user_model  # can also do from.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserAdminCreationForm, UserAdminChangeForm

User = get_user_model()


class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email')
    search_fields = ('first_name', 'last_name', 'email', 'username',)
    list_filter = ('is_passenger', 'is_flight_staff', 'is_finance')
    ordering = ['username']
    filter_horizontal = []

    form = UserAdminChangeForm  # for updating user in admin
    add_form = UserAdminCreationForm  # for creating user in admin

    fieldsets = (
        (None, {'fields': ()}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'username', 'password')}),
        # if you have any personal info fields e.g. names, include them as strings in the empty tuple.
        ('verification',
         {'fields': ('is_verified',)}),
        ('Permissions',
         {'fields': ('is_active', 'is_passenger', 'is_pilot', 'is_attendant', 'is_finance')})
    )
    '''
    add_fieldsets is not a standard ModelAdmin attribute. UserAdmin overides get_fieldsets
    to use this attribute when creating a user. '''
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2')
        }),
    )

    actions = ['make_active', 'make_inactive']

    def make_active(self, request, queryset):
        updated = queryset.update(is_active=True, is_archived=False, is_approved=True)
        self.message_user(request, ngettext(
            '%d User has successfully been marked as active.',
            '%d Users have been successfully marked as active.',
            updated,
        ) % updated, messages.SUCCESS)

    make_active.short_description = "Approve User"

    def make_inactive(self, request, queryset):
        updated = queryset.update(is_archived=True)
        self.message_user(request, ngettext(
            '%d User has been archived successfully.',
            '%d Users have been archived successfully.',
            updated,
        ) % updated, messages.INFO)

    make_inactive.short_description = "Archive User"

    def has_delete_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return True


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'image', 'gender', 'is_active', 'created', 'updated')
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


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('subject', 'message', 'created')
    list_filter = ('created',)
    search_fields = ('subject', 'message',)

    def has_delete_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return True


admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Feedback, FeedbackAdmin)
