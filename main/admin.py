from django.contrib import admin
from .models import User, Session, Data

# Register your models here.


@admin.register(User)
class UserAdmn(admin.ModelAdmin):
    list_display = ("username", "email")
    readonly_fields = ("created_at", "updated_at")


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ("user", "session")
    readonly_fields = ("created_at", "updated_at")


@admin.register(Data)
class DataAdmin(admin.ModelAdmin):
    list_display = ("user", "session", "data")
    readonly_fields = ("created_at", "updated_at")
