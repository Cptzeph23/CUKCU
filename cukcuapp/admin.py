from cloudinary.templatetags import cloudinary
from django.contrib import admin
from django.utils.html import format_html
from pyexpat.errors import messages
import cloudinary.uploader
from .models import TeamMember, Book, Leader, Contact, Exec


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

    def pdf_file_link(self, obj):
        if obj.pdf_file:
            # Use the get_pdf_url method instead of direct url access
            url = obj.get_pdf_url()
            if url:
                return format_html('<a href="{}" target="_blank">📄 View PDF</a>', url)
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



# --- Exec ADMIN ---
@admin.register(Exec)
class ExecAdmin(admin.ModelAdmin):
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