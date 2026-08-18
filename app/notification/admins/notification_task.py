from unfold.admin import ModelAdmin


class NotificationTaskAdmin(ModelAdmin):
    list_display = ["name", "provider", "event", "delivered_at", "created_at"]
    list_filter = ["provider", "name", "event"]
    list_select_related = ["event"]

    def has_change_permission(self, request, obj=None):
        return False
