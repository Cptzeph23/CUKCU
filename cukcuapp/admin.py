from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import TeamMember, Book, Leader
from django.utils.html import format_html

# admin.site.register(TeamMember)
# admin.site.register(Book)
# admin.site.register(Leader)

@admin.register(Leader)
class LeaderAdmin(admin.ModelAdmin):
    list_display = ('name', 'period', 'achievement', 'image_preview')
    search_fields = ('name', 'period')

    def image_preview(self, obj):
        if obj.image and hasattr(obj.image, 'url'):
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 4px;"/>', obj.image.url)
        return "No image"
    image_preview.short_description = "Preview"

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'upload_at')
    search_fields = ('title', 'author')

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'category')
    search_fields = ('name', 'position')


# @admin.register(Book)
# class BookAdmin(admin.ModelAdmin):
#     list_display = ('title', 'author', 'upload_at')
#     search_fields = ('title','author')
#     readonly_fields = ('upload_at',)

# @admin.register(Leader)
# class LeaderAdmin(admin.ModelAdmin):
#     list_display = ("name", "period", "achievement", "recommendation")
#     search_fields = ("name", "period")

