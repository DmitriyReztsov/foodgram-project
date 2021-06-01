from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    list_filter = ('email', 'username',)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
