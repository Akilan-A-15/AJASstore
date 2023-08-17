from django.contrib import admin
from .models import Catagory,Product

class CategoryAdmin(admin.ModelAdmin):
    list_display=('name','image')

admin.site.register(Catagory,CategoryAdmin)
admin.site.register(Product)