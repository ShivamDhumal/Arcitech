from django.contrib import admin
from .models import CustomUser ,content_item ,category

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(content_item)
admin.site.register(category)

