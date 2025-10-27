from django.contrib import admin
from .models import Ad, Review


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    """Отображение объявлений в админке"""
    list_display = ("id", "title", "price", "author", "created_at")
    list_filter = ("created_at", "price")
    search_fields = ("title", "description", "author__email")
    ordering = ("-created_at",)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Отображение отзывов в админке"""
    list_display = ("id", "text", "author", "ad", "created_at")
    list_filter = ("created_at", "ad")
    search_fields = ("text", "author__email", "ad__title")
    ordering = ("-created_at",)
