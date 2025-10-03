from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import TeamMember, Book, Leader

admin.site.register(TeamMember)
admin.site.register(Book)
admin.site.register(Leader)

# @admin.register(Book)
# class BookAdmin(admin.ModelAdmin):
#     list_display = ('title', 'author', 'upload_at')
#     search_fields = ('title','author')
#     readonly_fields = ('upload_at',)

# @admin.register(Leader)
# class LeaderAdmin(admin.ModelAdmin):
#     list_display = ("name", "period", "achievement", "recommendation")
#     search_fields = ("name", "period")

