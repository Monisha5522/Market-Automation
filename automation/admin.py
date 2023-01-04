from django.contrib import admin
from .views import User, Credential

# Register your models here.
admin.site.register(User)
admin.site.register(Credential)
