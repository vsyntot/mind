from django.contrib import admin
from users.models import *


class UserAdmin(admin.ModelAdmin):
    list_filter = ('role', 'is_staff', 'is_active', 'is_superuser')
    list_display = [field.name for field in User._meta.fields if field.name != 'password']

    def save_model(self, request, obj, form, change):
        if obj.pk:
            orig_obj = User.objects.get(pk=obj.pk)
            if obj.password != orig_obj.password:
                obj.set_password(obj.password)
        else:
            obj.set_password(obj.password)
        obj.save()


admin.site.register(User, UserAdmin)
