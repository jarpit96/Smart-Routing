from django.contrib import admin
from .models import State, Locality, District, PointOfInterests
# Register your models here.
admin.site.register(District)
admin.site.register(State)
admin.site.register(Locality)
admin.site.register(PointOfInterests)
