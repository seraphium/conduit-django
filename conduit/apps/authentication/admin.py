from django.contrib import admin
from conduit.apps.authentication.models import User

class UserAdmin(admin.ModelAdmin):
    
    list_display = ('name', 'permission', 'dept', 'line', 'phonenum')


admin.site.register(User, UserAdmin)


