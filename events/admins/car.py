from unfold.admin import ModelAdmin


class CarAdmin(ModelAdmin):
    list_display = ["brand", "model", "competitor__name"]
    list_filter = ["competitor__name"]

    def competitor_name(self, obj):
        return obj.competitor.name

    competitor_name.admin_order_field = 'competitor__name'
    competitor_name.short_description = 'Driver'
