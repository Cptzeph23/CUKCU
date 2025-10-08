from django.contrib import admin
from django.utils.html import format_html
from .models import TeamMember, Book, Leader, Contact


# --- CONTACT ADMIN ---
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'message')
    list_filter = ('name', 'email', 'subject')
    search_fields = ('name', 'email', 'subject')
    ordering = ('name',)


# --- LEADER ADMIN ---
@admin.register(Leader)
class LeaderAdmin(admin.ModelAdmin):
    list_display = ('name', 'period', 'achievement', 'image_preview')
    search_fields = ('name', 'period')

    def image_preview(self, obj):
        if obj.image:
            # CloudinaryField or ImageField both have .url attribute
            return format_html(
                '<img src="{}" width="60" height="60" style="border-radius:5px; object-fit:cover;"/>',
                obj.image.url
            )
        return "No image"

    image_preview.short_description = "Preview"


# --- BOOK ADMIN ---
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'upload_at', 'pdf_file_link')
    search_fields = ('title', 'author')
    readonly_fields = ('upload_at', 'pdf_file_link')

    def pdf_file_link(self, obj):
        if obj.pdf_file:
            return format_html('<a href="{}" target="_blank">📄 View PDF</a>', obj.pdf_file.url)
        return "No PDF"

    pdf_file_link.short_description = 'PDF File'

    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"


# --- TEAM MEMBER ADMIN ---
@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'category', 'image_preview')
    list_filter = ('category',)
    search_fields = ('name', 'position')

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="60" height="60" style="border-radius:5px; object-fit:cover;"/>',
                obj.image.url
            )
        return "No image"

    image_preview.short_description = "Preview"
