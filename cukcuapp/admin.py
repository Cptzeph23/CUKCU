from django.contrib import admin
from .models import TeamMember, Book, Leader
from django.utils.html import format_html

@admin.register(Leader)
class LeaderAdmin(admin.ModelAdmin):
    list_display = ('name', 'period', 'achievement', 'image_preview')
    search_fields = ('name', 'period')

    def image_preview(self, obj):
        if obj.image:
            # CloudinaryField provides url directly
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 4px;"/>', obj.image.url)
        return "No image"
    image_preview.short_description = "Preview"

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'upload_at', 'pdf_link')
    search_fields = ('title', 'author')

    def pdf_link(self, obj):
        if obj.pdf_file:
            return format_html('<a href="{}" target="_blank">Download PDF</a>', obj.pdf_file.url)
        return "No file"
    pdf_link.short_description = "PDF File"

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'category', 'image_preview')
    search_fields = ('name', 'position')

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 4px;"/>', obj.image.url)
        return "No image"
    image_preview.short_description = "Preview"