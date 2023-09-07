from django.contrib import admin

from bank.models import CommissionIncome


@admin.register(CommissionIncome)
class CommissionIncomeAdmin(admin.ModelAdmin):
    list_display = ('account', 'commission')
    readonly_fields = ('account', 'commission')
    actions = None

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

