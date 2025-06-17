from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import HangHoa
from .resources import HangHoaResource

class HangHoaAdmin(ImportExportModelAdmin):
    resource_class = HangHoaResource
    list_display = ('Name', 'qty', 'unitprice', 'totalamount')
    list_editable = ('qty', 'unitprice')
    list_display_links = None
    list_filter = ('Name',)
    search_fields = ('Name',)
# Register your models here.
admin.site.register(HangHoa, HangHoaAdmin)
