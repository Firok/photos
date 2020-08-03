from django.contrib import admin

from .models import Photo


class PhotoAdmin(admin.ModelAdmin):
    """
    Admin page view for Photo model
    """
    list_display = [
        'caption', 'photo',  'user', 'published_at',
        'created_at'
    ]
    date_hierarchy = 'created_at'
    fields = [
        'caption', 'photo', 'user', 'published_at',
        'created_at', 'updated_at'
    ]
    readonly_fields = [
        'created_at', 'updated_at'
    ]


admin.site.register(Photo, PhotoAdmin)
