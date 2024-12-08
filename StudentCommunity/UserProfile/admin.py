from django.contrib import admin
from django.contrib import admin
from .models import Feedback

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'submitted_at', 'message')
    search_fields = ('user__username', 'message')
    list_filter = ('submitted_at',)
# Register your models here.
