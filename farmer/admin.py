from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(User)
admin.site.register(Plant)
admin.site.register(Medium)
admin.site.register(Tray)