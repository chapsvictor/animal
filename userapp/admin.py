from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.html import format_html

from .models import User


admin.site.register(User)

# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#
#     def user_image(self, obj):
#         return format_html('<img src="{}" />'.format(obj.image.url))
#
#     user_image.short_description = 'Image'
#
#     list_display = ['user_image', 'email', 'username', 'first_name', 'last_name',]
