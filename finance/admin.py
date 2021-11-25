from django.contrib import admin, messages
from django.utils.translation import ngettext

from .models import Finance, FinanceProfile, FinanceFeedback, Payment


class FinanceAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'username')
    search_fields = ('first_name', 'last_name', 'email', 'username',)
    list_filter = ('is_active', 'is_archived', 'updated', 'created')

    actions = ['make_active', 'make_inactive']

    def make_active(self, request, queryset):
        updated = queryset.update(is_active=True, is_archived=False, is_verified=True)
        self.message_user(request, ngettext(
            '%d Finance manager has successfully been marked as active.',
            '%d Finance managers have been successfully marked as active.',
            updated,
        ) % updated, messages.SUCCESS)

    make_active.short_description = "Approve Finance manager"

    def make_inactive(self, request, queryset):
        updated = queryset.update(is_archived=True, is_active=False)
        self.message_user(request, ngettext(
            '%d Finance manager has been archived successfully.',
            '%d Finance managers have been archived successfully.',
            updated,
        ) % updated, messages.INFO)

    make_inactive.short_description = "Archive Finance manager"

    def has_delete_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return True


class FinanceProfileAdmin(admin.ModelAdmin):
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


class FinanceFeedbackAdmin(admin.ModelAdmin):
    list_display = ('subject', 'message', 'created')
    list_filter = ('created',)
    search_fields = ('subject', 'message',)

    def has_delete_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return True


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('booking', 'passenger', 'amount', 'mpesa', 'finance', 'is_confirmed', 'updated', 'created')
    list_filter = ('finance', 'is_confirmed',  'updated', 'created')
    search_fields = ('mpesa',)
    actions = ['make_confirmed']

    def make_confirmed(self, request, queryset):
        updated = queryset.update(is_confirmed=True)
        self.message_user(request, ngettext(
            '%d Payment has been confirmed successfully.',
            '%d Payment have been confirmed successfully.',
            updated,
        ) % updated, messages.SUCCESS)

    make_confirmed.short_description = "Confirm selected Payment"

    def has_delete_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return True


admin.site.register(Finance, FinanceAdmin)
admin.site.register(FinanceProfile, FinanceProfileAdmin)
admin.site.register(FinanceFeedback, FinanceFeedbackAdmin)
admin.site.register(Payment, PaymentAdmin)

