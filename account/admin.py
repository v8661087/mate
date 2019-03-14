from django.contrib import admin
from .models import Profile, Contact


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'photo', 'full_name',
                    'website', 'personal_profile', 'phone_number']


admin.site.register(Profile, ProfileAdmin)


class ContactAdmin(admin.ModelAdmin):
    list_display = ['user_from', 'user_to', 'created']


admin.site.register(Contact, ContactAdmin)



