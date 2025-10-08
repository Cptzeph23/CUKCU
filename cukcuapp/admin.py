from cloudinary.templatetags import cloudinary
from django.contrib import admin
from django.utils.html import format_html
from pyexpat.errors import messages

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
    list_display = ('title', 'author', 'uploaded_at', 'pdf_file_link')
    search_fields = ('title', 'author')
    readonly_fields = ('uploaded_at', 'pdf_file_link')

    def save_model(self, request, obj, form, change):
        pdf_file = request.FILES.get('pdf_file')
        if pdf_file:
            try:
                result = cloudinary.uploader.upload(
                    pdf_file,
                    resource_type='raw',
                    folder='books',
                    type='upload'
                )
                obj.pdf_file = result['secure_url']
            except Exception as e:
                messages.error(request, f"Cloudinary upload error: {e}")
        super().save_model(request, obj, form, change)

    def pdf_file_link(self, obj):
        if obj.pdf_file:
            return format_html('<a href="{}" target="_blank">📄 View PDF</a>', obj.pdf_file)
        return "No PDF"

    pdf_file_link.short_description = 'PDF File'


# --- TEAM MEMBER ADMIN ---
@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('order_index', 'name', 'position', 'category', 'image_preview')
    list_editable = ('order_index',)
    list_display_links = ('name',)
    list_filter = ('category',)
    search_fields = ('name', 'position')

    # Add this to make the admin list sortable by order_index
    sortable_by = ['order_index', 'name', 'position']

    # Add this to show the default sorting in admin
    ordering = ['order_index', 'name']

    def image_preview(self, obj):
        if obj.image:
            from django.utils.html import format_html
            return format_html(
                '<img src="{}" width="60" height="60" style="border-radius:5px; object-fit:cover;"/>',
                obj.image.url
            )
        return "No image"

    image_preview.short_description = "Preview"

    # Optional: Add actions for bulk ordering
    actions = ['reset_ordering']

    def reset_ordering(self, request, queryset):
        # Reset ordering for selected items
        for index, member in enumerate(queryset, start=1):
            member.order_index = index
            member.save()
        self.message_user(request, f"Reordered {queryset.count()} team members.")

    reset_ordering.short_description = "Reset ordering for selected items"