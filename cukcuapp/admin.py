from django.contrib import admin
from .models import TeamMember, Book, Leader, Contact
from django.utils.html import format_html


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'message')
    list_filter = ('name', 'email', 'subject')
    search_fields = ('name', 'email', 'subject')
    ordering = ('name',)

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
    readonly_fields = ('upload_at', 'pdf_link')

    def save_model(self, request, obj, form, change):
        # Handle file upload manually
        if 'pdf_file' in request.FILES:
            pdf_file = request.FILES['pdf_file']
            try:
                obj.upload_pdf(pdf_file)
                # Don't call super().save_model here as upload_pdf already saves
            except Exception as e:
                from django.contrib import messages
                messages.error(request, f"Error uploading PDF: {str(e)}")
        else:
            super().save_model(request, obj, form, change)

    def pdf_link(self, obj):
        if obj.pdf_url:
            return format_html(
                '<a href="{}" target="_blank" class="btn btn-sm btn-success">View PDF</a>'
                '<br><small>Public ID: {}</small>',
                obj.pdf_url,
                obj.pdf_public_id
            )
        return "No PDF uploaded"

    pdf_link.short_description = "PDF File"

    # Add a custom form field for PDF upload
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
            return f"<img src='{obj.image.url}' width='60' height='60' style='object-fit: cover; border-radius: 50%;' />"
        return "No image"
    image_preview.allow_tags = True
    image_preview.short_description = "Preview"
