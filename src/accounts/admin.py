from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "first_name", "is_seller", "is_owner")

admin.site.register(User, UserAdmin)
