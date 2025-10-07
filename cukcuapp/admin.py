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
    list_display = ('title', 'author', 'upload_at', 'pdf_preview')
    search_fields = ('title', 'author')
    readonly_fields = ('upload_at', 'pdf_preview')

    def pdf_preview(self, obj):
        if obj.pdf_file:
            return format_html(
                '<a href="{}" target="_blank" class="btn btn-sm btn-primary">View PDF</a> '
                '<span class="text-muted">({})</span>',
                obj.pdf_file.url,
                f"{obj.pdf_file.width}x{obj.pdf_file.height}" if hasattr(obj.pdf_file, 'width') else "PDF File"
            )
        return "No PDF uploaded"
    pdf_preview.short_description = "PDF File"

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'category', 'image_preview')
    search_fields = ('name', 'position')

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 4px;"/>', obj.image.url)
        return "No image"
    image_preview.short_description = "Preview"