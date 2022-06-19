from csv import list_dialects
from django.contrib import admin
from .models import Category, Products
# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Products)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price','stock' ,'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'slug': ('name',)}
