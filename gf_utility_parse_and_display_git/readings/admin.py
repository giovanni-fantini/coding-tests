from django.contrib import admin

from .models import Reading

@admin.register(Reading)
class ReadingAdmin(admin.ModelAdmin):
    search_fields = ['meter__mpan', 'meter__serial_number']
    
    def has_module_permission(self, request):
        return self.__check_is_staff(request)
    
    def has_view_permission(self, request, obj=None):
        return self.__check_is_staff(request)
    
    def has_change_permission(self, request, obj=None):
        return self.__check_is_staff(request)
    
    def __check_is_staff(self, request):
        if request.user.is_staff:
            return True
        else:
            return False