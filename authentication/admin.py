from django.contrib import admin
from django.contrib.auth.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = [f.name for f in User._meta.fields]


# admin.site.register(User, UserAdmin)
