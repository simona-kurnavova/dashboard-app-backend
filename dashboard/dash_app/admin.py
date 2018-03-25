from django.contrib import admin
from dash_app.models import *

# registration of models into administration
# admin accessible on /admin url

admin.site.register(App)
admin.site.register(Account)
admin.site.register(Dashboard)
admin.site.register(Widget)
