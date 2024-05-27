from django.contrib import admin
from projects.models import *


class ProjectAdmin(admin.ModelAdmin):
    list_filter = ('name', 'catalog', 'status')
    list_display = [field.name for field in Project._meta.fields if field.name not in ['description',
                                                                                       'url',
                                                                                       'image',
                                                                                       'model']]


admin.site.register(Project, ProjectAdmin)
