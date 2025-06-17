from import_export import resources
from .models import HangHoa

class HangHoaResource(resources.ModelResource):
    class Meta:
        model = HangHoa
        import_id_fields = ('Name',)
        fields = ('Name', 'qty', 'unitprice', 'totalamount')
        export_order = ('Name', 'qty', 'unitprice', 'totalamount')

   
