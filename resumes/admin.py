from django.contrib import admin

from resumes.models import Resume

# Register your models here.
@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('user', 'id', 'uid', 'content', 'updated_at')
    search_fields = ('user__username', 'id','uid', 'user__email', 'user__id')