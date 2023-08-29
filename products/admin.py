from django.contrib import admin

from .models import *

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    prepopulated_fields = {'slug': ('title',)}
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
