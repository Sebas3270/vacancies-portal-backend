from django.contrib import admin
from account.models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class UserInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Users'

class CustomUserAdmin (UserAdmin):
    inlines = (UserInline, )

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)