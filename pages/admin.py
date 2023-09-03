from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from .models import (
    Subject_A, Subject_B, Subject_C, Subject_D, Page,
)


class PageInline(GenericTabularInline):
    model = Page
    extra = 1


@admin.register(Subject_A)
class SubjectAAdmin(admin.ModelAdmin):
    inlines = [PageInline]


@admin.register(Subject_B)
class SubjectBAdmin(admin.ModelAdmin):
    inlines = [PageInline]


@admin.register(Subject_C)
class SubjectCAdmin(admin.ModelAdmin):
    inlines = [PageInline]


@admin.register(Subject_D)
class SubjectDAdmin(admin.ModelAdmin):
    inlines = [PageInline]


admin.site.register(Page)
