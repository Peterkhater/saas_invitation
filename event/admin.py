from django.contrib import admin
from .models import Event, EventGalleryImage, Pricing


admin.site.register(Event)
admin.site.register(EventGalleryImage)   
# Register your models here.
@admin.register(Pricing)
class PricingAdmin(admin.ModelAdmin):
    list_display = ('feature', 'min_value', 'max_value', 'price')
