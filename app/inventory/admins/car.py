from unfold.admin import ModelAdmin


class CarAdmin(ModelAdmin):
    list_display = ["brand", "model", "group", "competitor"]
    list_filter = ["brand", "group"]
    search_fields = ["brand", "model"]

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False
