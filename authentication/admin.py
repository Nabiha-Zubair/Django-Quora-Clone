from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register your models here.


class UserAdmin(admin.ModelAdmin):

    list_display = ('id', 'first_name', 'last_name', 'username',
                    'email', 'gender', 'is_email_verified', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Information', {
         'fields': ('gender', 'is_email_verified')}),
    )
    search_fields = ('username', 'email', 'is_staff')
    list_per_page = 15


admin.site.register(User, UserAdmin)
