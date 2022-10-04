from django.contrib import admin
from .models import *




admin.site.register(App)
admin.site.register(setting)
admin.site.site_header = "MONITORING SITE"
admin.site.site_title = "MONITORING SITE"
admin.site.index_title = " Welcome to MONITORING SITE"

