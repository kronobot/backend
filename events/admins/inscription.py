from unfold.admin import ModelAdmin


class InscriptionAdmin(ModelAdmin):
    list_display = ["event_name", "driver_name", "codriver_name", "car_name"]
    list_filter = ["event"]

    def event_name(self, obj):
        return obj.event.name
    event_name.short_description = 'Event'

    def driver_name(self, obj):
        return obj.driver.name
    event_name.short_description = 'Driver'

    def codriver_name(self, obj):
        return obj.codriver.name if obj.codriver else "-"
    codriver_name.short_description = 'Codriver'

    def car_name(self, obj):
        return f"{obj.car.brand} {obj.car.model}"

    car_name.short_description = 'Car'
